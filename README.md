# 🎬 Movie Ticket Booking System

## About the Project

This is a desktop-based **Movie Ticket Booking System** developed using **Python, Tkinter, and MySQL**. The main objective of this project is to provide a simple and user-friendly interface for booking movie tickets. Users can register, log in, search for movies, book tickets, view their booking history, cancel bookings, and receive ticket confirmation through email.

This project was developed as part of learning database connectivity, GUI development, and application programming using Python.

---

## Features

* User Registration
* User Login Authentication
* View Available Movies
* Search Movies
* Book Movie Tickets
* View Booking History
* Cancel Bookings
* Email Ticket Confirmation
* MySQL Database Integration
* Graphical User Interface using Tkinter

---

## Technologies Used

* Python 3.9
* Tkinter
* MySQL
* mysql-connector-python
* SMTP Email Service

---

## Project Structure

```text
MovieTicketBooking/
│
├── main.py
├── current_gui.py
├── booking.py
├── database.py
├── email_sender.py
├── email_ticket.py
├── movie_ticket.py
├── movies.py
├── user.py
├── movie_booking.sql
├── requirements.txt
├── screenshots/
│   ├── homepage.png
│   ├── login.png
│   ├── register.png
│   ├── book tickets.png
│   └── booking_history.png
└── README.md
```

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ramyasreedegala2024/MovieTicketBooking.git
cd MovieTicketBooking
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL Database

Open MySQL and create a database:

```sql
CREATE DATABASE movie_booking;
USE movie_booking;
SOURCE movie_booking.sql;
```

### 4. Run the Application

```bash
python current_gui.py
```

---

## Screenshots

### Home Page

![Homepage](screenshots/homepage.png)

### Login Page

![Login](screenshots/login.png)

### Registration Page

![Register](screenshots/register.png)

### Ticket Booking

![Book Tickets](screenshots/book%20tickets.png)

### Booking History

![Booking History](screenshots/booking_history.png)

---

## Functionalities Implemented

* User authentication and registration
* Movie search functionality
* Ticket booking system
* Booking cancellation
* Booking history management
* Email confirmation service
* Database operations using MySQL
* Interactive GUI application

---

## Future Improvements

* Online payment gateway integration
* Admin dashboard
* Seat selection system
* Movie posters and trailers
* QR code ticket generation
* Cloud database support

---

## Author

**Ramya Sree Degala**

GitHub: https://github.com/ramyasreedegala2024
