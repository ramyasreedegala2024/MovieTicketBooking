CREATE DATABASE movie_booking;

USE movie_booking;

CREATE TABLE users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100),
    security_answer VARCHAR(100)
);

CREATE TABLE movies(
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(100),
    show_time VARCHAR(50),
    available_seats INT,
    ticket_price DECIMAL(10,2)
);

CREATE TABLE bookings(
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    seat_number VARCHAR(20),
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);