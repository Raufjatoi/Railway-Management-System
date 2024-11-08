# Railway Management System

> [!WARNING]
> This project is currently in development 🙂 ( everythin works tho )

> [!NOTE]
> This is a CRUD-based project developed as part of the **Database Management System** coursework, created by a team comprising [Ahsan](https://github.com/MrAhsan777), [Umar](https://github.com/Umarkeerio), and [Rehman](#).

## Project Overview
The Railway Management System is a web application designed to streamline train management and booking processes. The system includes features for both **admin users** and **regular users**, providing a user-friendly interface for booking trains and managing records.

### Roles & Access Levels
1. **Admin**:
   - Admin users can add, edit, or delete train records and view all user bookings.
   - Admins have additional control to manage train schedules and booking data.
2. **User**:
   - Regular users can browse available trains, book tickets, and manage their bookings.
   - Each user can view and cancel their own bookings.

## Features

- **➕ Add Trains (Admin)**: Admins can add new train records by providing essential details like departure and arrival times, route, and pricing.
- **👁️ View Trains**: Lists all available trains with details such as departure time, arrival time, price, and available seats. Users can choose from these options to book their journeys.
- **✏️ Edit Trains (Admin)**: Admins can update train information, such as schedule, price, and seat availability.
- **🗑️ Delete Trains (Admin)**: Admins can remove train records from the system.
- **📅 Book Tickets (User)**: Users can book tickets for available trains based on real-time data.
- **🔍 View Bookings (User)**: Each user can view their booking history, including train details.
- **❌ Cancel Bookings (User)**: Users can cancel their own bookings if needed.

## Setup Instructions

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the application**:
    ```bash
    streamlit run app.py
    ```

3. **Database Setup**:
    - Ensure the database (`rail.db`) is correctly configured with the following tables:
        - `Users` table for storing user accounts with roles (`admin` or `user`).
        - `Trains` table for train information.
        - `Bookings` table to manage ticket bookings.
    - This setup enables user registration, login, and booking features to function as intended.

## Upcoming Features

> [!IMPORTANT]
> The project is continuously evolving, with new features and enhancements planned.

For a more detailed look at the project structure, refer to the [project structure document](https://github.com/Raufjatoi/Railway-Management-System/structure.txt).
