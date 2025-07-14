import streamlit as st
from db import connect_db
import pandas as pd
import sqlite3
from datetime import datetime

conn = connect_db()
c = conn.cursor()

st.markdown("<h2 style='text-align: center;'>📝 Create New Order</h2>", unsafe_allow_html=True)

try:
    employees_df = pd.read_sql_query("SELECT id, name FROM personnel", conn)
    menu_items_df = pd.read_sql_query("SELECT id, name, price FROM menuitems", conn)
except Exception as e:
    st.error(f"Error fetching data from the database: {e}")
    st.stop()

with st.form("create_order_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        #Select employee
        employee_id = st.selectbox("Employee in Charge", options=employees_df['id'], format_func=lambda x: employees_df[employees_df['id'] == x]['name'].values[0])
    
    with col2:
        #Select menu item
        table_options = ['M1', 'M2', 'M3', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'B1', 'B2', 'B3', 'B4', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6']
        table_number = st.selectbox("Table Number", options=table_options) 
    
    selected_items = st.multiselect(
        "Select Menu Items",
        options=menu_items_df['id'],
        format_func=lambda x: menu_items_df[menu_items_df['id'] == x]['name'].values[0]
    )

    submit_button = st.form_submit_button("Create Order")


    if submit_button:
        if not selected_items:
            st.warning("Please select at least one menu item.")
        else:
            try:
                # Calculate total price
                total_price = menu_items_df[menu_items_df['id'].isin(selected_items)]['price'].sum()

                order_status = "Pending"
                current_time = datetime.now()

                #Obtain the id of the order
                c.execute("INSERT INTO orders (personnel_id, table_number, date, status, total) VALUES (?, ?, ?, ?, ?)", (employee_id, table_number, current_time, order_status, total_price))

                new_order_id = c.lastrowid # Get the last inserted order ID

                for item_id in selected_items:
                    item_price = menu_items_df[menu_items_df['id'] == item_id]['price'].iloc[0]
                    c.execute("INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES (?, ?, ?, ?)", (new_order_id, item_id, 1, item_price))
                conn.commit()
                st.success(f"Order #{new_order_id} for table {table_number} has been created successfully!")
                st.balloons()
            except sqlite3.Error as e:
                st.error(f"An error occurred while creating the order: {e}")

st.markdown("---")

st.markdown("<h2 style='text-align: center;'>🔥 Active Orders</h2>", unsafe_allow_html=True)

try: 
    active_orders_df = pd.read_sql_query("SELECT * FROM orders WHERE status = 'Pending' ORDER BY date ASC", conn)
    if active_orders_df.empty:
        st.write("No active orders at the moment.")
    else:
        for index, order in active_orders_df.iterrows(): # Iterate through each order
            with st.container(border = True):
                st.markdown(f"**Order #{order['id']}** | Table **{order['table_number']}** | **{order['date']}**")

                details_df = pd.read_sql_query(f"""SELECT od.quantity, mi.name FROM order_details od JOIN menuitems mi ON od.menu_item_id = mi.id WHERE od.order_id = {order['id']}""", conn)

                for _, detail in details_df.iterrows():
                    st.text(f"- {detail['quantity']} x {detail['name']}")
                
                order_time = pd.to_datetime(order['date'])
                st.caption(f"Received at: {order_time.strftime('%Y-%m-%d %H:%M')}")
                payment_method = st.selectbox("Select Payment Method", ["Cash", "Credit Card", "QR Code", "IC Card"], key=f"payment_method_{order['id']}")
                st.markdown(f"**Total Amount:** ¥{order['total']:.2f}")


                # --- Finalize order and regiter payment ---

                if st.button(f"Finalize Order and Register Payment", key = f"finish_order_{order['id']}"):
                    try:
                        #1. Update order status to 'Completed'
                        c.execute("UPDATE orders SET status = 'Completed' WHERE id = ?", (order['id'],))
                        #2. Insert the register in the payments table
                        sale_time = datetime.now()
                        total_amount = order['total']
                        c.execute("INSERT INTO sales (order_id, sale_time, total_amount, payment_method) VALUES (?, ?, ?, ?)", (order['id'], sale_time, total_amount, payment_method))

                        conn.commit()
                        st.success(f"Order #{order['id']} has been finalized and payment registered successfully!")
                        
                        #3. Update the page
                        st.rerun()
                    except sqlite3.Error as e:
                        st.error(f"An error occurred while finalizing the order: {e}")
except sqlite3.Error as e:
    st.error(f"Could not display active orders: {e}")

st.markdown("---")

# --- Sell History ---

st.markdown("<h2 style='text-align: center;'>📜 Sell History</h2>", unsafe_allow_html=True)

try:
    recent_sales_df = pd.read_sql_query("SELECT s.sale_id, s.sale_time, s.total_amount, s.payment_method, o.table_number FROM sales s JOIN orders o ON s.order_id = o.id ORDER BY s.sale_time DESC", conn)
    if recent_sales_df.empty:
        st.write("No sales history available.")
    else:
        st.dataframe(recent_sales_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Could not display recent sales: {e}")

# Close the database connection
conn.close()



