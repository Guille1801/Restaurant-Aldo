import streamlit as st
from db import connect_db
import pandas as pd
import sqlite3

st.markdown("<h1 style='text-align: center;'>Reports</h1>", unsafe_allow_html=True)

conn = connect_db()
c = conn.cursor()

st.markdown("---")

# --- Sales Report ---
st.markdown("<h2 style='text-align: center;'>Sales Report</h2>", unsafe_allow_html=True)
try:
    sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
    if not sales_df.empty:
        sales_df['sale_time'] = pd.to_datetime(sales_df['sale_time'])
        sales_df['date'] = sales_df['sale_time'].dt.date
        sales_summary = sales_df.groupby('date').agg({'total_amount': 'sum'}).reset_index()
        
        st.dataframe(sales_summary, use_container_width=True, hide_index=True)
        
        total_sales = sales_summary['total_amount'].sum()
        st.markdown(f"**Total Sales Amount:** ¥{total_sales:.2f}")
    else:
        st.write("No sales data available.")
except sqlite3.Error as e:
    st.error(f"An error occurred while fetching sales data: {e}")

# --- Orders Report ---
st.markdown("<h2 style='text-align: center;'>Orders Report</h2>", unsafe_allow_html=True)

try:
    orders_df = pd.read_sql_query("SELECT * FROM orders", conn)
    if not orders_df.empty:
        orders_df['date'] = pd.to_datetime(orders_df['date']).dt.date
        orders_summary = orders_df.groupby('date').agg({'total': 'sum', 'id': 'count'}).rename(columns={'id': 'order_count'}).reset_index()
        
        st.dataframe(orders_summary, use_container_width=True, hide_index=True)
        
        total_orders = orders_summary['order_count'].sum()
        total_revenue = orders_summary['total'].sum()
        st.markdown(f"**Total Orders:** {total_orders}")
        st.markdown(f"**Total Revenue:** ¥{total_revenue:.2f}")
    else:
        st.write("No orders data available.")
except sqlite3.Error as e:
    st.error(f"An error occurred while fetching orders data: {e}")