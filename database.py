import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Ramya@123",
    database="movie_booking"
)

cursor = conn.cursor(buffered=True)