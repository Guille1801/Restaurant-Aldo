import streamlit as st
from db import connect_db
import pandas as pd
import sqlite3
import altair as alt

st.markdown("<h1 style='text-align: center;'>Dishes and Drinks Inventory</h1>", unsafe_allow_html=True)

conn = connect_db()
c = conn.cursor()

st.markdown("---")

# --- Dish List ---

st.markdown("### Dishes List")

filter_dish = st.selectbox("Select a dish category to filter", ["All", "Soup", "Salad", "Sea Food", "Hot Appetizer", "Meat/Chicken", "Cold Appetizer", "Dessert", "Other"], key="dish_filter")
c.execute("SELECT * FROM menuitems WHERE type = 'dish' AND (category = ? OR ? = 'All')", (filter_dish, filter_dish))
rows = c.fetchall()
columns = [desc[0] for desc in c.description]  # Esto obtiene los nombres reales
df = pd.DataFrame(rows, columns=columns)
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
    # --- Dish Information ---

    df_counter = df.shape[0]

    df_average_price = df["price"].mean()

    st.write(f"You have {df_counter} {filter_dish.lower()} dishes and the **average price is ¥{int(df_average_price)}.**")
    st.write(f"The **most expensive dish is {df['name'][df['price'].idxmax()]}** with a price of ¥{int(df['price'].max())}.")
    st.write(f"The **cheapest dish is {df['name'][df['price'].idxmin()]}** with a price of ¥{int(df['price'].min())}.")

    

    
else:
    st.write("No dishes found.")

st.markdown("---")
# --- Drinks List ---

st.markdown("### Drinks List")

filter_drink = st.selectbox("Select a drink type to filter", ["All", "Pisco", "Macerado", "Pisco Cocktail", "Beer", "Rum", "Peruvian Wine", "Tabernero", "Tacama", "Other Wines", "Soft Drinks", "Others"], key="drink_filter")
c.execute("SELECT * FROM menuitems WHERE type = 'drink' AND (category = ? OR ? = 'All')", (filter_drink, filter_drink))
rows = c.fetchall()
columns = [desc[0] for desc in c.description]  # Esto obtiene los nombres
df = pd.DataFrame(rows, columns=columns)
# reales
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
    # --- Drink Information ---
    df_counter = df.shape[0]
    df_average_price = df["price"].mean()

    st.write(f"You have {df_counter} {st.session_state.drink_filter.lower()} and the **average price is ¥{int(df_average_price)}.**")
    st.write(f"The **most expensive {filter_drink} is {df['name'][df['price'].idxmax()]}** with a price of ¥{int(df['price'].max())}.")
    st.write(f"The **cheapest {filter_drink} is {df['name'][df['price'].idxmin()]}** with a price of ¥{int(df['price'].min())}.")
else:
    st.write("No drinks found.")


conn.close()

