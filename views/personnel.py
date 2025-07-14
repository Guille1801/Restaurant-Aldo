import streamlit as st
from db import connect_db
import pandas as pd
import sqlite3

st.markdown("<h1 style='text-align: center;'>Personnel Management</h1>", unsafe_allow_html=True)

conn = connect_db()
c = conn.cursor()

#--- Show Personnel List ---

st.markdown("### Personnel List")

contract_filter = st.selectbox("Select a contract type to filter", 
            ["All", "Admin", "Full-time", "Part-time"], 
            key="contract_filter")

c.execute("SELECT * FROM personnel WHERE contract_type = ? OR ? = 'All'", 
          (st.session_state.contract_filter, st.session_state.contract_filter))
personnel = c.fetchall()
columns = [desc[0] for desc in c.description]  # Esto obtiene los nombres reales
df = pd.DataFrame(personnel, columns=columns)
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("No personnel found.")

#--- salary overview ---

st.markdown("### Salary Overview Personnel")

if not df.empty:
    salary_overview = st.selectbox("Select a contract type to filter", 
                 ["Full-time", "Part-time"], 
                 key="salary_filter")
    
    if salary_overview == "Full-time":

        st.markdown("#### Total and Average Salary for Full-time Personnel")
        full_time_df = df[df['contract_type'] == 'Full-time']
        if not full_time_df.empty:
            total_salary = int(full_time_df['salary'].sum())
            average_salary = int(full_time_df['salary'].mean())
            st.markdown(f"**Total Salary for Full-time Personnel per month:** ¥{total_salary}")
            st.markdown(f"**Average Salary for Full-time Personnel per montg:** ¥{average_salary}")
        else:
            st.warning("No full-time personnel found.")
    else:
    
        st.markdown("#### Total and Average Salary for Part-time Personnel")
        part_time_df = df[df['contract_type'] == 'Part-time']
        if not part_time_df.empty:
            total_salary = int(part_time_df['salary'].sum())
            average_salary = int(part_time_df['salary'].mean())
            st.markdown(f"**Total Salary for Part-time Personnel per hour:** ¥{total_salary}")
            st.markdown(f"**Average Salary for Part-time Personnel per hour:** ¥{average_salary}")
        else:
            st.warning("No part-time personnel found.")