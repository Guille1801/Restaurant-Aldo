import pickle
from pathlib import Path
#from generate_keys import names, usernames

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="Aldo's System", page_icon="🔐")

st.sidebar.image("Aldo Profile.jpg", caption = "Aldo's System", use_container_width=True)


### ---USER AUTHENTICATION SETUP ---

file_path = Path(__file__).parent / "hashed_passwords.pkl"
with file_path.open("rb") as file:
    credentials = pickle.load(file)

authenticator = stauth.Authenticate(
    credentials,
    "restaurant_auth",
    "abcd",
    cookie_expiry_days=30,
)

# Obtener el estado de la autenticación
auth_status = st.session_state.get("authentication_status")
username    = st.session_state.get("username")
name        = st.session_state.get("name")

authenticator.login("main", "Login")

if auth_status == False:
    st.error("Username/password is incorrect")

if auth_status == None:
    st.warning("Please enter your username and password")



if auth_status == True:

    #--- PAGE SET UP ---
    main_page = st.Page(
        page = "views/main_app.py",
        title = "Main Menu",
        icon = "🌐",
        default= True,
    )

    orders_page = st.Page(
        page = "views/orders.py",
        title = "Orders",
        icon = "📝",
    )

    inventory_page = st.Page(
        page = "views/inventory.py",
        title = "Inventory",
        icon = "📦",
    )

    personnel_page = st.Page(
        page = "views/personnel.py",
        title = "Personnel",
        icon = "👥",
    )

    reports_page = st.Page(
        page = "views/reports.py",
        title = "Reports",
        icon = "📊",
    )

    settings_page = st.Page(
        page = "views/settings.py",
        title = "Settings",
        icon = "⚙️",
    )

    pg = st.navigation(pages = [main_page, orders_page, inventory_page, personnel_page, reports_page, settings_page])


    pg.run()

    # Logout button

    authenticator.logout("Logout", "sidebar")