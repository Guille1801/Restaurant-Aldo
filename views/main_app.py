import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path
from db import connect_db
import pandas as pd
from datetime import datetime
conn = connect_db()
c = conn.cursor()

# --- graph function ---

def plot_pie_chart(df, title):
    if df.empty:
        st.info(f"No data available to plot: {title}")
        return
        
    fig, ax = plt.subplots()
    ax.pie(
        df['total_amount'],
        labels=df['category'],
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.85,
    )
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')
    plt.title(title)
    st.pyplot(fig)

def plot_bar_chart(df, x_col, y_col, title, xlabel, ylabel, color='skyblue'):
    if df.empty:
        st.info(f"No data available to plot: {title}")
        return

    fig, ax = plt.subplots()
    ax.bar(df[x_col], df[y_col], color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

conn = connect_db() 
c = conn.cursor()

st.markdown(f"<h1 style='text-align: center;'>Welcome to Aldo Peru's System {st.session_state.get('name', '')}! 🌐</h1>", unsafe_allow_html=True)
st.markdown("---")

selected_date = st.date_input("Select a date to view sales", datetime.today())

st.markdown(f"<h3 style='text-align: center;'>Sales Overview for {selected_date.strftime('%Y-%m-%d')}</h3>", unsafe_allow_html=True)

try:
    sales_query = "SELECT * FROM sales WHERE date(sale_time) = ?"
    sales_df = pd.read_sql_query(sales_query, conn, params=(selected_date,))

    if sales_df.empty:
        st.info("No sales data available for the selected date.")
    else:
        sales_df['sale_time'] = pd.to_datetime(sales_df['sale_time'])

        with st.expander("View Sales Data for Selected Date", expanded=True):
            total_sales = sales_df['total_amount'].sum()
            st.metric(label="Total Sales Amount", value=f"¥{total_sales:,.2f}")
            st.dataframe(sales_df[['sale_time', 'total_amount', 'payment_method']], use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("<h3 style='text-align: center;'>Sales Graphs</h3>", unsafe_allow_html=True)

        sales_graph_type = st.selectbox("Select a sales graph", ["Sales by Payment Method", "Orders by Hour", "Sales by Employee"])
        
        if sales_graph_type == "Sales by Payment Method":
            sales_by_payment = sales_df.groupby('payment_method')['total_amount'].sum().reset_index()
            plot_bar_chart(sales_by_payment, 'payment_method', 'total_amount', 'Sales by Payment Method', 'Payment Method', 'Total Amount (¥)')
        
        elif sales_graph_type == "Orders by Hour":
            sales_df['hour'] = sales_df['sale_time'].dt.hour
            orders_by_hour = sales_df.groupby('hour').size().reindex(range(24), fill_value=0)
            st.line_chart(orders_by_hour, y_label="Number of Orders")

        elif sales_graph_type == "Sales by Employee":
            employee_query = """
                SELECT p.name, SUM(s.total_amount) AS total_amount
                FROM sales s
                JOIN orders o ON s.order_id = o.id
                JOIN personnel p ON o.personnel_id = p.id
                WHERE date(s.sale_time) = ?
                GROUP BY p.name
            """
            employee_sales = pd.read_sql_query(employee_query, conn, params=(selected_date,))
            plot_bar_chart(employee_sales, 'name', 'total_amount', 'Sales by Employee', 'Employee Name', 'Total Amount (¥)', color='lightgreen')

        st.markdown("---")

        # --- Gráficos de Ventas por Categoría de Producto ---
        st.markdown("<h3 style='text-align: center;'>Sales by Product Category</h3>", unsafe_allow_html=True)
        category_type = st.selectbox("Select a category to view sales", ["Food", "Drink"])

        item_type_to_query = 'dish' if category_type == "Food" else 'drink'
        
        category_query = """
            SELECT mi.category, SUM(od.quantity * od.item_price) AS total_amount
            FROM order_details od
            JOIN menuitems mi ON od.menu_item_id = mi.id
            JOIN orders o ON od.order_id = o.id
            WHERE o.status = 'Completed' AND date(o.date) = ? AND mi.type = ?
            GROUP BY mi.category
        """
        category_sales_df = pd.read_sql_query(category_query, conn, params=(selected_date, item_type_to_query))
        plot_pie_chart(category_sales_df, f"Sales by {category_type} Category")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:

            # --- Drink Sold Today ---
            st.markdown("---")
            st.markdown(f"### Drinks Sold on {selected_date.strftime('%Y-%m-%d')}")
            drinks_sold = pd.read_sql_query("""
                SELECT mi.name, mi.category, SUM(od.quantity) AS total_quantity
                    FROM order_details od
                    JOIN menuitems mi ON od.menu_item_id = mi.id
                    JOIN orders o ON od.order_id = o.id
                    WHERE o.status = 'Completed' AND date(o.date) = ? AND mi.type = 'drink'
                    GROUP BY mi.name
                """, conn, params=(selected_date,))
            selected_drink = st.selectbox("Select a drink type to view details", ["All" ,"Pisco", "Macerado", "Pisco Cocktail", "Beer", "Rum", "Peruvian Wine", "Tabernero", "Tacama", "Other Wines", "Soft Drinks", "Others"], key='drink_type_filter')
            if selected_drink != 'All':
                fig, ax = plt.subplots()
                filtered_drinks = drinks_sold[drinks_sold['category'] == selected_drink]
                if filtered_drinks.empty:
                    st.write(f"No drinks sold on {selected_date} in the category: {selected_drink}")
                else:
                    ax.bar(filtered_drinks['name'], filtered_drinks['total_quantity'], color='orange')
                    ax.set_title(f'Drinks Sold Today - {selected_drink}')
                    ax.set_xlabel('Drink Name')
                    ax.set_ylabel('Total Quantity Sold')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
            else:
                fig, ax = plt.subplots()
                drinks_sold = drinks_sold.sort_values(by='total_quantity', ascending=False).head(10)
                ax.bar(drinks_sold['name'], drinks_sold['total_quantity'], color='orange')
                ax.set_title('Drinks Sold Today - All Types')
                ax.set_xlabel('Drink Name')
                ax.set_ylabel('Total Quantity Sold')
                plt.xticks(rotation=45)
                st.pyplot(fig)
        with col2:
            # --- Dish Sold Today ---
            st.markdown("---")

            st.markdown(f"### Dishes Sold on {selected_date.strftime('%Y-%m-%d')}")
            dishes_sold = pd.read_sql_query("""
                SELECT mi.name, mi.category, SUM(od.quantity) AS total_quantity
                FROM order_details od
                JOIN menuitems mi ON od.menu_item_id = mi.id
                JOIN orders o ON od.order_id = o.id
                WHERE o.status = 'Completed' AND date(o.date) = ? AND mi.type = 'dish'
                GROUP BY mi.name
            """, conn, params=(selected_date,))

            selected_dish = st.selectbox("Select a dish category to view details", ["All", "Soup", "Salad", "Sea Food", "Hot Appetizer", "Meat/Chicken", "Cold Appetizer", "Dessert", "Other"], key='dish_type_filter')
            if selected_dish != 'All':
                fig, ax = plt.subplots()
                filtered_dishes = dishes_sold[dishes_sold['category'] == selected_dish]
                if filtered_dishes.empty:
                    st.write(f"No dishes sold on {selected_date} in the category: {selected_dish}")
                else:
                    ax.bar(filtered_dishes['name'], filtered_dishes['total_quantity'], color='lightblue')
                    ax.set_title(f'Dishes Sold Today - {selected_dish}')
                    ax.set_xlabel('Dish Name')
                    ax.set_ylabel('Total Quantity Sold')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
            else:
                fig, ax = plt.subplots()
                dishes_sold = dishes_sold.sort_values(by='total_quantity', ascending=False).head(10)
                ax.bar(dishes_sold['name'], dishes_sold['total_quantity'], color='lightblue')
                ax.set_title('Dishes Sold Today - All Types')
                ax.set_xlabel('Dish Name')
                ax.set_ylabel('Total Quantity Sold')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            

except Exception as e:
    st.error(f"An error occurred while fetching sales data: {e}")
finally:
    if conn:
        conn.close()
