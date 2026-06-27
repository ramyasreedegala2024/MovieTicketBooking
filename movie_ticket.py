import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="ramya123@mysql",
    database="movie_booking"
)

cursor = conn.cursor(buffered=True)

current_user = None


def signup():

    print("\n===== SIGN UP =====")

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    try:
        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )

        conn.commit()

        print("Registration Successful!")

    except mysql.connector.Error as err:
        print("Error:", err)


def login():

    global current_user

    print("\n===== LOGIN =====")

    email = input("Enter Email: ")
    password = input("Enter Password: ")

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()

    if user:
        current_user = user
        print("\nLogin Successful!")
        print("Welcome,", user[1])

    else:
        print("Invalid Email or Password")


def logout():

    global current_user

    if current_user:
        current_user = None
        print("Logged Out Successfully!")
    else:
        print("No User Logged In")


def view_movies():

    cursor.execute("SELECT * FROM movies")

    movies = cursor.fetchall()

    print("\n===== AVAILABLE MOVIES =====\n")

    if not movies:
        print("No Movies Available")
        return

    for movie in movies:
        print(
            f"Movie ID: {movie[0]} | "
            f"Movie Name: {movie[1]} | "
            f"Show Time: {movie[2]} | "
            f"Available Seats: {movie[3]}"
        )


def book_ticket():

    global current_user

    if current_user is None:
        print("Please Login First!")
        return

    try:
        movie_id = int(input("Enter Movie ID: "))
    except ValueError:
        print("Enter Valid Movie ID!")
        return

    seat = input("Enter Seat Number: ")

    cursor.execute(
        "SELECT * FROM bookings WHERE movie_id=%s AND seat_number=%s",
        (movie_id, seat)
    )

    booked = cursor.fetchone()

    if booked:
        print("Seat Already Booked!")
        return

    cursor.execute(
        "SELECT available_seats FROM movies WHERE movie_id=%s",
        (movie_id,)
    )

    movie = cursor.fetchone()

    if movie is None:
        print("Movie Not Found!")
        return

    if movie[0] <= 0:
        print("No Seats Available!")
        return

    cursor.execute(
        """
        INSERT INTO bookings(user_id,movie_id,seat_number)
        VALUES(%s,%s,%s)
        """,
        (current_user[0], movie_id, seat)
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


def my_bookings():

    global current_user

    if current_user is None:
        print("Please Login First!")
        return

    cursor.execute(
        """
        SELECT booking_id,movie_id,seat_number
        FROM bookings
        WHERE user_id=%s
        """,
        (current_user[0],)
    )

    bookings = cursor.fetchall()

    print("\n===== MY BOOKINGS =====\n")

    if not bookings:
        print("No Bookings Found")
        return

    for booking in bookings:
        print(
            f"Booking ID: {booking[0]} | "
            f"Movie ID: {booking[1]} | "
            f"Seat: {booking[2]}"
        )


def cancel_ticket():

    global current_user

    if current_user is None:
        print("Please Login First!")
        return

    try:
        booking_id = int(input("Enter Booking ID: "))
    except ValueError:
        print("Invalid Booking ID!")
        return

    cursor.execute(
        "SELECT movie_id FROM bookings WHERE booking_id=%s AND user_id=%s",
        (booking_id, current_user[0])
    )

    booking = cursor.fetchone()

    if not booking:
        print("Booking Not Found!")
        return

    movie_id = booking[0]

    cursor.execute(
        "DELETE FROM bookings WHERE booking_id=%s",
        (booking_id,)
    )

    cursor.execute(
        """
        UPDATE movies
        SET available_seats = available_seats + 1
        WHERE movie_id=%s
        """,
        (movie_id,)
    )

    conn.commit()

    print("Ticket Cancelled Successfully!")


def add_movie():

    movie_name = input("Enter Movie Name: ")
    show_time = input("Enter Show Time: ")

    try:
        seats = int(input("Enter Available Seats: "))
    except ValueError:
        print("Enter Valid Number!")
        return

    cursor.execute(
        """
        INSERT INTO movies(movie_name,show_time,available_seats)
        VALUES(%s,%s,%s)
        """,
        (movie_name, show_time, seats)
    )

    conn.commit()

    print("Movie Added Successfully!")


def delete_movie():

    try:
        movie_id = int(input("Enter Movie ID: "))
    except ValueError:
        print("Invalid Movie ID!")
        return

    cursor.execute(
        "DELETE FROM movies WHERE movie_id=%s",
        (movie_id,)
    )

    conn.commit()

    print("Movie Deleted Successfully!")


while True:

    print("\n===== MOVIE BOOKING SYSTEM =====")
    print("1. Sign Up")
    print("2. Login")
    print("3. View Movies")
    print("4. Book Ticket")
    print("5. My Bookings")
    print("6. Cancel Ticket")
    print("7. Logout")
    print("8. Add Movie")
    print("9. Delete Movie")
    print("10. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        signup()

    elif choice == "2":
        login()

    elif choice == "3":
        view_movies()

    elif choice == "4":
        book_ticket()

    elif choice == "5":
        my_bookings()

    elif choice == "6":
        cancel_ticket()

    elif choice == "7":
        logout()

    elif choice == "8":
        add_movie()

    elif choice == "9":
        delete_movie()

    elif choice == "10":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")

cursor.close()
conn.close()