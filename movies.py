from database import *

def add_movie():

    name = input("Movie Name: ")
    time = input("Show Time: ")
    seats = int(input("Seats: "))

    cursor.execute(
        """
        INSERT INTO movies(movie_name,show_time,available_seats)
        VALUES(%s,%s,%s)
        """,
        (name,time,seats)
    )

    conn.commit()

    print("Movie Added Successfully!")


def view_movies():

    cursor.execute("SELECT * FROM movies")

    movies = cursor.fetchall()

    print("\n===== MOVIES =====\n")

    for movie in movies:
        print(movie)


def search_movie():

    name = input("Enter Movie Name: ")

    cursor.execute(
        """
        SELECT * FROM movies
        WHERE movie_name LIKE %s
        """,
        ("%" + name + "%",)
    )

    movies = cursor.fetchall()

    if not movies:
        print("Movie Not Found!")
        return

    for movie in movies:
        print(movie)