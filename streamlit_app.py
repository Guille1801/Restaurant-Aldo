import streamlit as st

#--- PAGE SET UP ---

login_page = st.Page(
    page = "login.py",
    title = "Login",
    icon = "🔐",
    default= True,
)

main_page = st.Page(
    page = "views/main_app.py",
    title = "Main Menu",
    icon = "🌐",
)

orders_page = st.Page(
    page = "views/orders.py",
    title = "Orders",
    icon = "🍳",
)

inventory_page = st.Page(
    page = "views/inventory.py",
    title = "Dishes & Drinks",
    icon = "🍸",
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