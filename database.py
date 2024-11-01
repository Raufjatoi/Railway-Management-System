import sqlite3

def create_database():
    conn = sqlite3.connect('railway_management.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS train (
                    train_id INTEGER PRIMARY KEY,
                    name TEXT,
                    train_type TEXT,
                    start_time TEXT,
                    end_time TEXT)''')
    conn.commit()
    conn.close()

def add_train(train_id, name, train_type, start_time, end_time):
    conn = sqlite3.connect('railway_management.db')
    c = conn.cursor()
    c.execute("INSERT INTO train (train_id, name, train_type, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
              (train_id, name, train_type, start_time, end_time))
    conn.commit()
    conn.close()

def view_trains():
    conn = sqlite3.connect('railway_management.db')
    c = conn.cursor()
    c.execute("SELECT * FROM train")
    trains = c.fetchall()
    conn.close()
    return trains

def edit_train(train_id, new_name, new_type, new_start, new_end):
    conn = sqlite3.connect('railway_management.db')
    c = conn.cursor()
    c.execute("UPDATE train SET name=?, train_type=?, start_time=?, end_time=? WHERE train_id=?",
              (new_name, new_type, new_start, new_end, train_id))
    conn.commit()
    conn.close()

def delete_train(train_id):
    conn = sqlite3.connect('railway_management.db')
    c = conn.cursor()
    c.execute("DELETE FROM train WHERE train_id=?", (train_id,))
    conn.commit()
    conn.close()
