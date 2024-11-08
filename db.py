import sqlite3 as sql

c = sql.connect("rail.db")
cur = c.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user' -- User roles ('user' or 'admin')
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Stations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    location TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Trains (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    from_station TEXT NOT NULL,
    to_station TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    price REAL NOT NULL,
    seats_available INTEGER NOT NULL,
    added_by INTEGER, -- Links to the ID of the user (admin) who added the train
    FOREIGN KEY (added_by) REFERENCES Users (id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    train_id INTEGER,
    booking_time TEXT,
    FOREIGN KEY (user_id) REFERENCES Users (id),
    FOREIGN KEY (train_id) REFERENCES Trains (id)
)
""")

c.commit()

stations = [
    ('Nawabshah Station', 'Nawabshah'),
    ('Karachi Station', 'Karachi'),
    ('Lahore Station', 'Lahore'),
    ('Multan Station', 'Multan'),
    ('Hyderabad Station', 'Hyderabad')
]
cur.executemany("INSERT OR IGNORE INTO Stations (name, location) VALUES (?, ?)", stations)

users = [
    ('Rauf', '32', 'admin'),  # im admin
    ('Umar', '66', 'user'), 
    ('Ahsan', '45', 'user'),
    ('Rehman', '65', 'user'),
    ('Meer', '47', 'user')
]
cur.executemany("INSERT OR IGNORE INTO Users (username, password, role) VALUES (?, ?, ?)", users)

c.commit()

cur.execute("SELECT id FROM Users WHERE username = 'Rauf' AND role = 'admin'")
result = cur.fetchone()
admin_id = result[0] if result else None

if admin_id:
    trains = [
        ('Karachi Express', 'Nawabshah Station', 'Karachi Station', '08:00', '10:00', 1000.00, 100, admin_id),
        ('Tezgam', 'Lahore Station', 'Karachi Station', '09:00', '15:00', 4700.00, 80, admin_id),
        ('Green Line', 'Multan Station', 'Karachi Station', '10:30', '12:30', 1600.00, 50, admin_id),
        ('Hyderabad Junction', 'Hyderabad Station', 'Lahore Station', '11:00', '13:00', 5550.00, 60, admin_id),
        ('Islamabad Express', 'Karachi Station', 'Islamabad Station', '07:00', '14:00', 4800.00, 40, admin_id)
    ]
    cur.executemany("""
        INSERT OR IGNORE INTO Trains (name, from_station, to_station, departure_time, arrival_time, price, seats_available, added_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, trains)
else:
    print("Admin user 'Rauf' not found. Please ensure the admin user is added before adding trains.")

c.commit()
c.close()

print('done')