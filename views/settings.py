import streamlit as st
from db import connect_db
import pandas as pd
import sqlite3

conn = connect_db()
c = conn.cursor()

# --- some extra functions ---

def generate_employee_id(contract):

    employee_id_range = {
        "Admin": (1001, 1999),
        "Full-time": (2001, 2999),
        "Part-time": (3001, 3999)
    }

    if contract not in employee_id_range:
        return None
    
    range_start, range_end = employee_id_range[contract]

    query = "SELECT MAX(id) FROM personnel WHERE id BETWEEN ? AND ?"

    c.execute(query, (range_start, range_end))
    result = c.fetchone()[0]

    if result is None:
        new_id = range_start
    else:
        new_id = result + 1

        if new_id > range_end:
            st.error(f"Cannot generate new ID for {contract} employees. Maximum ID reached.")
            return None
    return new_id

# --- Page Title ---
st.markdown("<h1 style='text-align: center;'>Add/Edit Page</h1>", unsafe_allow_html=True)
st.markdown("---")


# --- Add New Information ---

st.markdown("<h2 style='text-align: center;'>Add Dish/Drink</h2>", unsafe_allow_html=True)

# ---Separate in columns---

col1, col2 = st.columns(2, gap="large")

with col1:

    st.markdown("#### Add a New Dish")

    with st.form("add_dish_form"):

        dish_name = st.text_input("Dish Name")
        price = st.number_input("Price", min_value=0.0)
        dish_category = st.selectbox("Dish Type",  ["Soup", "Salad", "Sea Food", "Hot Appetizer", "Meat/Chicken", "Cold Appetizer", "Dessert", "Other"], key="dish_type")

        if st.form_submit_button("Add Dish"):
            c.execute("INSERT INTO menuitems (name, type, category, price) VALUES (?, ?, ?, ?)", (dish_name, "dish", dish_category, price))
            conn.commit()
            st.success(f"Dish '{dish_name}' added successfully!")

with col2:


    st.markdown("#### Add a New Drink")

    with st.form("add_drink_form"):

        drink_name = st.text_input("Drink Name")
        drink_price = st.number_input("Drink Price", min_value=0.0)
        drink_category = st.selectbox("Drink Type", ["Pisco", "Macerado", "Pisco Cocktail", "Beer", "Rum", "Peruvian Wine", "Tabernero", "Tacama", "Other Wines", "Soft Drinks", "Others"])

        if st.form_submit_button("Add Drink"):
            c.execute("INSERT INTO menuitems (name, type, category, price) VALUES (?, ?, ?, ?)", (drink_name, "drink", drink_category, drink_price))
            conn.commit()
            st.success(f"Drink '{drink_name}' added successfully!")

st.markdown("---")


st.markdown("<h2 style='text-align: center;'> Update Dish/Drink Information</h2>", unsafe_allow_html=True)

#--- Separate in columns ---

col1, col2 = st.columns(2, gap="large")

with col1:

#--- Edit Dish ---


    c.execute("SELECT * FROM menuitems WHERE type = 'dish'")
    dishes = c.fetchall()

    st.markdown("#### Edit a Dish")

    # Convertir a DataFrame
    columns = [desc[0] for desc in c.description]
    df = pd.DataFrame(dishes, columns = columns)
    dish_names = df["name"].tolist()

    if not dish_names:
        st.warning("No dish available to edit.")
    else:
        selected_dish = st.selectbox("Select a dish to edit", dish_names, key = 'dish_selector')

        dish_row = df[df["name"] == selected_dish].iloc[0]
        dish_id = int(dish_row["id"])
        options =  ["Soup", "Salad", "Sea Food", "Hot Appetizer", "Meat/Chicken", "Cold Appetizer", "Dessert", "Other"]
        # Intentar encontrar el índice. Si no está, poner 0 como predeterminado
        try:
            default_index = options.index(dish_row["type"])
        except ValueError:
            default_index = 0
        
        #--- form ---

        with st.form(key="edit_dish_form"):
            new_dish_name = st.text_input("New Dish Name", value=dish_row["name"], key = "edit_dish_name")
            new_dish_price = st.number_input("New Dish Price", min_value = 0.0, value=dish_row["price"], key = "edit_dish_price")
            new_dish_category = st.selectbox("New Dish Category", options, index = default_index, key = "edit_dish_category")

            submitted = st.form_submit_button("Update Dish")

            if submitted:
                c.execute("UPDATE menuitems SET name = ?, price = ?, category = ? WHERE id = ?", (new_dish_name, new_dish_price, new_dish_category, dish_id))
                conn.commit()
                st.success(f"Dish '{new_dish_name}' updated successfully!")
                #st.rerun()  # Refresh the page to show updated data

with col2:

#--- Edit Drink Details ---

    c.execute("SELECT * FROM menuitems WHERE type = 'drink'")
    drinks = c.fetchall()

    st.markdown("#### Edit a Drink")

    # Convertir a DataFrame
    columns = [desc[0] for desc in c.description]
    df_drinks = pd.DataFrame(drinks, columns = columns)
    drink_names = df_drinks["name"].tolist()

    if not drink_names:
        st.warning("No drinks available to edit.")
    else:
        selected_drink = st.selectbox("Select a drink to edit", drink_names, key = 'drink_selector')

        drink_row = df_drinks[df_drinks["name"] == selected_drink].iloc[0]
        drink_id = int(drink_row["id"])
        options = ["Pisco", "Macerado", "Pisco Cocktail", "Beer", "Rum", "Peruvian Wine", "Tabernero", "Tacama", "Other Wines", "Soft Drinks", "Others"]
        # Intentar encontrar el índice. Si no está, poner 0 como predeterminado
        try:
            default_index = options.index(drink_row["type"])
        except ValueError:
            default_index = 0

        #--- form ---

        with st.form(key="edit_drink_form"):


            new_drink_name = st.text_input("New Drink Name", value=drink_row["name"], key = "edit_drink_name")
            new_drink_price = st.number_input("New Drink Price", min_value = 0.0, value=drink_row["price"], key = "edit_drink_price")
            new_drink_category = st.selectbox("New Drink Type", options, index = default_index, key = "edit_drink_type")

            submitted = st.form_submit_button("Update Drink")

            if submitted:
                c.execute("UPDATE menuitems SET name = ?, price = ?, category = ? WHERE id = ?", (new_drink_name, new_drink_price, new_drink_category, drink_id))
                conn.commit()
                st.success(f"Drink '{new_drink_name}' updated successfully!")
                #st.rerun()  # Refresh the page to show updated data

### --- Add Employee Section --- ###

st.markdown("<h2 style='text-align: center;'> Add New Employee</h2>", unsafe_allow_html=True)



c.execute("SELECT * FROM personnel")
personnel = c.fetchall()

contract_type = st.selectbox("Contract Type", ["Admin", "Full-time", "Part-time"])        

st.markdown("### Add Employee")
with st.form("add_employee_form", clear_on_submit=True):
    

    employee_name = st.text_input("Employee Name", placeholder="Takeru Takeda")
    start_date = st.date_input("Start Date")
    phone_number = st.text_input("Phone Number", placeholder = "09012345678")
    email = st.text_input("Email", placeholder = "takerutakeda@gmail.com")
    position = st.text_input("Position", placeholder = "Enter position (e.g., Bartender, Waiter)")
    if contract_type == "Part-time":
        salary = st.number_input("Hourly Wage", min_value=0, value=1200, step=50, format="%d")
    else:
        salary = st.number_input("Monthly Salary", min_value=0, value=260000, step=10000, format="%d")
    
    
    employee_id = generate_employee_id(contract_type)

    submitted = st.form_submit_button("Add Employee")

    if submitted:
        if not employee_name:
            st.error("Please enter an employee name.")
        else:
            new_id = generate_employee_id(contract_type)

            if new_id:
                try:
                    insert_query = "INSERT INTO personnel (id, name, contract_type, start_date, phone, email, position, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    c.execute(insert_query, (new_id, employee_name, contract_type, start_date, phone_number, email, position, salary))
                    conn.commit()
                    st.success(f"Employee '{employee_name}' added successfully with ID {new_id}!")
                except sqlite3.Error as e:
                    st.error(f"An error occurred while adding the employee: {e}")
            else:
                st.error(f"Could not generate a new ID for {contract_type} employees. Maximum ID reached.")

conn.close()
