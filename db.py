import sqlite3

DB_NAME = 'finances.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS credit_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        bank TEXT,
        balance REAL NOT NULL,
        apr REAL NOT NULL,
        min_payment REAL,
        user_notes TEXT
    );

    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        lender TEXT,
        balance REAL NOT NULL,
        apr REAL NOT NULL,
        min_payment REAL,
        user_notes TEXT
    );

    CREATE TABLE IF NOT EXISTS capital_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        account_type TEXT NOT NULL CHECK(account_type IN ('checking', 'savings', 'retirement')),
        balance REAL NOT NULL,
        user_notes TEXT
    );

    CREATE TABLE IF NOT EXISTS houses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        house_type TEXT NOT NULL CHECK(house_type IN ('quad', 'tri', 'duplex', 'single')),
        price REAL NOT NULL,
        est_rent_per_unit REAL,
        user_notes TEXT
    );
    ''')

    conn.commit()
    conn.close()
