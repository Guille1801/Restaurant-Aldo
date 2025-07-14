import streamlit as st
from db import connect_db

st.title("Add New Information")

dish_name = st.text_input("Dish Name")
price = st.number_input("Price", min_value=0.0)

if st.button("Add Dish"):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO dish (name, price) VALUES (?, ?)", (dish_name, price))
    conn.commit()
    conn.close()
    st.success(f"Dish '{dish_name}' added successfully!")

drink_name = st.text_input("Drink Name")
drink_price = st.number_input("Drink Price", min_value=0.0)

if st.button("Add Drink"):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO drinks (name, price) VALUES (?, ?)", (drink_name, drink_price))
    conn.commit()
    conn.close()
    st.success(f"Drink '{drink_name}' added successfully!")



