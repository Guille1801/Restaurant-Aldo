import sqlite3

def connect_db():
    #Connect to the SQLite database
    return sqlite3.connect('restaurant.db', check_same_thread=False, timeout=10)
    

def create_tables(conn):
    c = conn.cursor()
    # items table
    c.execute('''
    CREATE TABLE IF NOT EXISTS menuitems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT CHECK(type IN ('dish', 'drink')),
            category TEXT NOT NULL,
            price REAL NOT NULL)
              ''')
    # Personnel table
    c.execute('''
    CREATE TABLE IF NOT EXISTS personnel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contract_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL)
              ''')
    # orders table
    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,  
            table_number INTEGER,
            personnel_id INTEGER,
            total REAL,
            FOREIGN KEY (personnel_id) REFERENCES personnel(id))
            
              ''')
    # order details table
    c.execute('''
    CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            menu_item_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id))
            
            
              ''')
    # sale table
    c.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        sale_time DATETIME,
        total_amount REAL,
        payment_method TEXT,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )
    ''')

    conn.commit()


def initialize_db():
    conn = connect_db()
    create_tables(conn)
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print("Database initialized and tables created.")