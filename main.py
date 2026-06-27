from user import register, login, change_password, forgot_password
from movies import add_movie, view_movies, search_movie
from booking import book_ticket, booking_history, cancel_ticket

while True:

    print("\n===== MOVIE TICKET BOOKING SYSTEM =====")
    print("1. Register")
    print("2. Login")
    print("3. Add Movie")
    print("4. View Movies")
    print("5. Search Movie")
    print("6. Book Ticket")
    print("7. Booking History")
    print("8. Cancel Ticket")
    print("9. Change Password")
    print("10. Forgot Password")
    print("11. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        register()

    elif choice == "2":
        login()

    elif choice == "3":
        add_movie()

    elif choice == "4":
        view_movies()

    elif choice == "5":
        search_movie()

    elif choice == "6":
        book_ticket()

    elif choice == "7":
        booking_history()

    elif choice == "8":
        cancel_ticket()

    elif choice == "9":
        change_password()

    elif choice == "10":
        forgot_password()

    elif choice == "11":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")