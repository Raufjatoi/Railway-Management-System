import streamlit as s
import sqlite3 as sql
import base64 as b

# Database connection
c = sql.connect('rail.db')
cur = c.cursor()

# Functions to manage trains
def get_trains():
    cur.execute('SELECT * FROM Trains')
    return cur.fetchall()

def add_train(name, from_station, to_station, departure_time, arrival_time, price, seats_available, added_by):
    cur.execute(
        '''
        INSERT INTO Trains (name, from_station, to_station, departure_time, arrival_time, price, seats_available, added_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (name, from_station, to_station, departure_time, arrival_time, price, seats_available, added_by)
    )
    c.commit()

def update_train(train_id, seats_available):
    cur.execute(
        'UPDATE Trains SET seats_available = ? WHERE id = ?',
        (seats_available, train_id)
    )
    c.commit()

def delete_train(train_id):
    cur.execute('DELETE FROM Trains WHERE id = ?', (train_id,))
    c.commit()

# Functions for booking management
def book_train(user_id, train_id):
    cur.execute('SELECT seats_available FROM Trains WHERE id = ?', (train_id,))
    seats = cur.fetchone()[0]
    if seats > 0:
        cur.execute(
            'INSERT INTO Bookings (user_id, train_id, booking_time) VALUES (?, ?, datetime("now"))',
            (user_id, train_id)
        )
        update_train(train_id, seats - 1)
        c.commit()
        return True
    return False

def cancel_booking(booking_id, train_id):
    cur.execute('DELETE FROM Bookings WHERE id = ?', (booking_id,))
    cur.execute('SELECT seats_available FROM Trains WHERE id = ?', (train_id,))
    seats = cur.fetchone()[0]
    update_train(train_id, seats + 1)
    c.commit()

def get_user_bookings(user_id):
    cur.execute(
        """
        SELECT Bookings.id, Trains.name 
        FROM Bookings 
        JOIN Trains ON Bookings.train_id = Trains.id 
        WHERE Bookings.user_id = ?
        """, 
        (user_id,)
    )
    return cur.fetchall()

def get_all_bookings():
    cur.execute(
        """
        SELECT Bookings.id, Users.username, Trains.name 
        FROM Bookings 
        JOIN Trains ON Bookings.train_id = Trains.id 
        JOIN Users ON Bookings.user_id = Users.id
        """
    )
    return cur.fetchall()


# User profile and authentication
def sign_up(username, password, role='user'):
    try:
        cur.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        c.commit()
        return True
    except sql.IntegrityError:
        return False

def sign_in(username, password):
    cur.execute('SELECT id, username, role FROM Users WHERE username = ? AND password = ?', (username, password))
    return cur.fetchone()

# Set the background
def set_background(png_file):
    with open(png_file, "rb") as image:
        encoded_image = b.b64encode(image.read()).decode()
        css = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
        }}
        </style>
        '''
        s.markdown(css, unsafe_allow_html=True)

set_background('rail1.png')

# Session state management
if 'user_authenticated' not in s.session_state:
    s.session_state.user_authenticated = False
    s.session_state.username = ""
    s.session_state.user_id = None
    s.session_state.role = 'user'
    s.session_state.show_signup = False
    s.session_state.page = "login"

s.title("Railway Management System")

# Profile Section
if s.session_state.user_authenticated:
    with s.sidebar:
        s.header("Profile")
        s.write(f"Username: {s.session_state.username}")
        s.write(f"Role: {s.session_state.role}")

if s.session_state.page == "login":
    if s.session_state.show_signup:
        s.header("Create Account")
        signup_username = s.text_input("Choose a Username", key="signup_username")
        signup_password = s.text_input("Choose a Password", type='password', key="signup_password")
        if s.button("Sign Up"):
            if sign_up(signup_username, signup_password):
                s.success("Account created successfully! Please log in.")
                s.session_state.show_signup = False
            else:
                s.error("Username already exists. Please choose a different one.")
        if s.button("Back to Login"):
            s.session_state.show_signup = False
    else:
        s.header("Login")
        login_username = s.text_input("Enter Username", key="login_username")
        login_password = s.text_input("Enter Password", type='password', key="login_password")
        if s.button("Login"):
            user = sign_in(login_username, login_password)
            if user:
                s.session_state.user_authenticated = True
                s.session_state.username = user[1]
                s.session_state.user_id = user[0]
                s.session_state.role = user[2]
                s.success(f"Hello, {user[1]}!")
                s.session_state.page = "main"
                s.rerun()
            else:
                s.error("Invalid username or password.")
        if s.button("Don't have an account? Create one"):
            s.session_state.show_signup = True

elif s.session_state.page == "main":
    s.write(f"Welcome, {s.session_state.username}!")

    if s.session_state.role == 'admin':
        s.header("Admin Panel")
        s.subheader("Add a New Train")
        name = s.text_input("Train Name")
        from_station = s.text_input("From Station")
        to_station = s.text_input("To Station")
        departure_time = s.text_input("Departure Time (YYYY-MM-DD HH:MM)")
        arrival_time = s.text_input("Arrival Time (YYYY-MM-DD HH:MM)")
        price = s.number_input("Ticket Price", min_value=0.0)
        seats_available = s.number_input("Seats Available", min_value=1, step=1)

        if s.button("Add Train"):
            add_train(name, from_station, to_station, departure_time, arrival_time, price, seats_available, s.session_state.user_id)
            s.success("Train added successfully!")

        s.subheader("Update or Remove Trains")
        trains = get_trains()
        for train in trains:
            train_id, name, from_station, to_station, departure_time, arrival_time, price, seats_available, _ = train
            s.write(f"Train: {name} | From: {from_station} | To: {to_station}")
            s.write(f"Seats Available: {seats_available}")
            new_seats = s.number_input(f"Update Seats for {name}", value=seats_available, step=1)
            if s.button(f"Update Train {train_id}", key=f"update_{train_id}"):
                update_train(train_id, new_seats)
                s.success(f"Train {name} updated successfully!")
            if s.button(f"Remove Train {train_id}", key=f"remove_{train_id}"):
                delete_train(train_id)
                s.success(f"Train {name} removed successfully!")

    s.header("Available Trains")
    for train in get_trains():
        train_id, name, from_station, to_station, departure_time, arrival_time, price, seats_available, _ = train
        s.subheader(f"Train Name: {name}")
        s.write(f"From: {from_station} | To: {to_station}")
        s.write(f"Departure: {departure_time} | Arrival: {arrival_time}")
        s.write(f"Price: Rs{price:.2f} | Seats Available: {seats_available}")
        if s.button(f"Book {name}", key=f"book_{train_id}"):
            if book_train(s.session_state.user_id, train_id):
                s.success(f"You have successfully booked {name}!")
            else:
                s.error(f"Sorry, no seats available for {name}.")
            
    if s.session_state.role == 'admin':
        s.subheader("All User Bookings")
        all_bookings = get_all_bookings()
        for booking in all_bookings:
            booking_id, username, train_name = booking
            s.write(f"Booking ID: {booking_id} - User: {username} - Train: {train_name}")
                       
    s.header("Your Bookings")
    user_bookings = get_user_bookings(s.session_state.user_id)
    for booking in user_bookings:
        booking_id, train_name = booking
        s.write(f"Booking ID: {booking_id} - Train: {train_name}")
        if s.button(f"Cancel Booking {booking_id}", key=f"cancel_{booking_id}"):
            cancel_booking(booking_id, train_id)
            s.success(f"Booking {booking_id} has been canceled.")

    if s.button("Log Out"):
        s.session_state.user_authenticated = False
        s.session_state.username = ""
        s.session_state.user_id = None
        s.session_state.page = "login"
        s.rerun() 