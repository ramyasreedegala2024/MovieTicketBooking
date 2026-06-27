from database import *

def book_ticket():

    try:
        movie_id = int(input("Movie ID: "))
        user_id = int(input("User ID: "))
    except ValueError:
        print("Invalid Input!")
        return

    seat = input("Seat Number: ").upper()

    try:
        tickets = int(input("Number of Tickets: "))
    except ValueError:
        print("Invalid Number!")
        return

    cursor.execute(
        """
        SELECT available_seats,ticket_price
        FROM movies
        WHERE movie_id=%s
        """,
        (movie_id,)
    )

    movie = cursor.fetchone()

    if not movie:
        print("Movie Not Found!")
        return

    available_seats = movie[0]
    ticket_price = float(movie[1] or 0)

    if available_seats <= 0:
        print("No Seats Available!")
        return

    cursor.execute(
        """
        SELECT * FROM bookings
        WHERE movie_id=%s AND seat_number=%s
        """,
        (movie_id,seat)
    )

    if cursor.fetchone():
        print("Seat Already Booked!")
        return

    amount = tickets * ticket_price

    print("\nTicket Price:", ticket_price)
    print("Total Amount:", amount)

    cursor.execute(
        """
        INSERT INTO bookings(user_id,movie_id,seat_number)
        VALUES(%s,%s,%s)
        """,
        (user_id,movie_id,seat)
    )

    cursor.execute(
        """
        UPDATE movies
        SET available_seats = available_seats - 1
        WHERE movie_id=%s
        """,
        (movie_id,)
    )

    conn.commit()

    print("Ticket Booked Successfully!")


def booking_history():

    user_id = int(input("Enter User ID: "))

    cursor.execute(
        "SELECT * FROM bookings WHERE user_id=%s",
        (user_id,)
    )

    bookings = cursor.fetchall()

    if not bookings:
        print("No Bookings Found")
        return

    print("\n===== BOOKING HISTORY =====\n")

    for booking in bookings:
        print(booking)


def cancel_ticket():

    booking_id = int(input("Enter Booking ID: "))

    cursor.execute(
        "DELETE FROM bookings WHERE booking_id=%s",
        (booking_id,)
    )

    conn.commit()

    print("Ticket Cancelled Successfully!")