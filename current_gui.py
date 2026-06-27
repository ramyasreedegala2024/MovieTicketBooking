import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from database import *
from email_sender import send_ticket
from pdf_ticket import generate_ticket
BTN_FONT = ("Segoe UI", 11, "bold")
window = tk.Tk()
window.title("Movie Ticket Booking System")
window.geometry("700x950")
window.state("zoomed")

BTN_BG = "#1e293b"
BTN_FG = "white"
BTN_ACTIVE = "#334155"

button_style = {
    "width": 25,
    "height": 1,
    "bg": BTN_BG,
    "fg": BTN_FG,
    "activebackground": BTN_ACTIVE,
    "activeforeground": "white",
    "font": ("Segoe UI", 11, "bold"),
    "bd": 0,
    "cursor": "hand2"
}

window.configure(bg="#0f172a")
current_user = None
def is_admin():

    if current_user is None:
        return False

    return current_user[5] == "admin"

# ---------------- REGISTER ---------------- #

def register():

    reg = tk.Toplevel(window)
    reg.title("Register")
    reg.geometry("350x300")

    tk.Label(reg, text="Name").pack()
    name_entry = tk.Entry(reg)
    name_entry.pack()

    tk.Label(reg, text="Email").pack()
    email_entry = tk.Entry(reg)
    email_entry.pack()

    tk.Label(reg, text="Password").pack()
    password_entry = tk.Entry(reg, show="*")
    password_entry.pack()

    tk.Label(reg, text="Security Answer").pack()
    security_entry = tk.Entry(reg)
    security_entry.pack()

    def save_user():

        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        security_answer = security_entry.get()

        try:

            cursor.execute(
                """
                INSERT INTO users(name,email,password,security_answer)
                VALUES(%s,%s,%s,%s)
                """,
                (name, email, password, security_answer)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Registration Successful"
            )

            reg.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Button(
        reg,
        text="Register",
        command=save_user,
        **button_style
    ).pack(pady=15)
# ---------------- FORGOT PASSWORD ---------------- #

def forgot_password():

    email = simpledialog.askstring(
        "Forgot Password",
        "Enter Your Email"
    )

    if not email:
        return

    answer = simpledialog.askstring(
        "Security Answer",
        "Enter Your Security Answer"
    )

    if not answer:
        return

    cursor.execute("""
        SELECT password
        FROM users
        WHERE email=%s
        AND security_answer=%s
    """, (email, answer))

    user = cursor.fetchone()

    if user:
        messagebox.showinfo(
            "Password Found",
            f"Your Password is: {user[0]}"
        )
    else:
        messagebox.showerror(
            "Error",
            "Invalid Email or Security Answer"
        )
# ---------------- LOGIN ---------------- #

def login():

    login_window = tk.Toplevel(window)
    login_window.title("Login")
    login_window.geometry("350x250")

    tk.Label(login_window, text="Email").pack(pady=5)
    email_entry = tk.Entry(login_window, width=30)
    email_entry.pack()

    tk.Label(login_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", width=30)
    password_entry.pack()

    def check_login():

        global current_user

        email = email_entry.get()
        password = password_entry.get()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email=%s AND password=%s
            """,
            (email, password)
        )

        user = cursor.fetchone()

        if user:

            current_user = user
            login_btn.pack_forget()
            logout_btn.pack(before=exit_btn, pady=8)

            welcome_label.config(
    text=f"Welcome, {user[1]}"
)

            messagebox.showinfo(
                "Success",
                f"Welcome {user[1]}"
            )

            # Show admin buttons only for admin users
            if user[5] == "admin":

                add_movie_btn.pack(pady=8)
                delete_movie_btn.pack(pady=8)
                update_movie_btn.pack(pady=8)
                view_all_bookings_btn.pack(pady=8)
                admin_dashboard_btn.pack(pady=8)

            login_window.destroy()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Login"
            )

    tk.Button(
        login_window,
        text="Login",
        command=check_login,
        **button_style
    ).pack(pady=15)

    tk.Button(
        login_window,
        text="Forgot Password",
        command=forgot_password,
        **button_style
    ).pack(pady=8)

# ---------------- BOOK TICKET ---------------- #
def book_ticket():

    if current_user is None:
        messagebox.showerror(
            "Login Required",
            "Please login first."
        )
        return

    ticket_window = tk.Toplevel(window)
    ticket_window.title("Book Ticket")
    ticket_window.geometry("350x300")

    tk.Label(ticket_window, text="Movie ID").pack(pady=5)
    movie_entry = tk.Entry(ticket_window, width=30)
    movie_entry.pack()

    tk.Label(ticket_window, text="Seat Number").pack(pady=5)
    seat_entry = tk.Entry(ticket_window, width=30)
    seat_entry.pack()

    def confirm_booking():

        movie_id = movie_entry.get()
        seat_number = seat_entry.get()

        if movie_id == "" or seat_number == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

        cursor.execute(
            "SELECT available_seats FROM movies WHERE movie_id=%s",
            (movie_id,)
        )

        movie = cursor.fetchone()

        if movie is None:
            messagebox.showerror("Error", "Movie not found")
            return

        if movie[0] <= 0:
            messagebox.showerror("Error", "No seats available")
            return

        cursor.execute(
            """
            INSERT INTO bookings(user_id, movie_id, seat_number)
            VALUES(%s, %s, %s)
            """,
            (current_user[0], movie_id, seat_number)
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

        messagebox.showinfo(
            "Success",
            "Ticket Booked Successfully!"
        )

        ticket_window.destroy()

    tk.Button(
        ticket_window,
        text="Book Ticket",
        command=confirm_booking,
        **button_style
    ).pack(pady=20)
# ---------------- VIEW MOVIES ---------------- #

def view_movies():

    movie_window = tk.Toplevel(window)
    movie_window.title("Movies")
    movie_window.geometry("700x350")

    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    if not movies:
        tk.Label(
            movie_window,
            text="No Movies Available"
        ).pack(pady=20)
        return

    for movie in movies:

        text = (
            f"Movie ID: {movie[0]} | "
            f"Movie Name: {movie[1]} | "
            f"Show Time: {movie[2]} | "
            f"Seats: {movie[3]} | "
            f"Ticket Price: {movie[4]}"
        )

        tk.Label(
            movie_window,
            text=text,
            font=("Arial", 11)
        ).pack(pady=5)
        

# ---------------- ADMIN - ADD MOVIE ---------------- #

def add_movie():

    if not is_admin():
        messagebox.showerror(
            "Access Denied",
            "Only Admin can access this feature."
        )
        return

    admin = tk.Toplevel(window)
    admin.title("Add Movie")
    admin.geometry("350x300")

    tk.Label(admin, text="Movie Name").pack()
    movie_name = tk.Entry(admin)
    movie_name.pack()

    tk.Label(admin, text="Show Time").pack()
    show_time = tk.Entry(admin)
    show_time.pack()

    tk.Label(admin, text="Available Seats").pack()
    seats = tk.Entry(admin)
    seats.pack()

    tk.Label(admin, text="Ticket Price").pack()
    ticket_price = tk.Entry(admin)
    ticket_price.pack()
    
    def save_movie():

        try:

            cursor.execute(
                """
                INSERT INTO movies
                (movie_name, show_time, available_seats, ticket_price)
                VALUES(%s,%s,%s,%s)
                """,
                (
                    movie_name.get(),
                    show_time.get(),
                    seats.get(),
                    ticket_price.get()
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Movie Added Successfully"
            )

            admin.destroy()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        admin,
        text="Add Movie",
        command=save_movie,
        **button_style
    ).pack(pady=20) 

# ---------------- ADMIN - DELETE MOVIE ---------------- #
def delete_movie():
        if not is_admin():
         messagebox.showerror(
            "Access Denied",
            "Only Admin can access this feature."
        )
        return

        movie_id = simpledialog.askstring(
        "Delete Movie",
        "Enter Movie ID"
    )

        if not movie_id:
         return

        cursor.execute(
        """
        DELETE FROM movies
        WHERE movie_id=%s
        """,
        (movie_id,)
    )

        conn.commit()

        messagebox.showinfo(
        "Success",
        "Movie Deleted"
    )
# ---------------- UPDATE MOVIE ---------------- #

def update_movie():
        if not is_admin():
         messagebox.showerror(
            "Access Denied",
            "Only Admin can access this feature."
        )
        return

        movie_id = simpledialog.askstring(
        "Update Movie",
        "Enter Movie ID"
    )

        if not movie_id:
         return

        new_name = simpledialog.askstring(
         "Movie Name",
        "Enter New Movie Name"
    )

        new_show = simpledialog.askstring(
        "Show Time",
        "Enter New Show Time"
    )

        new_price = simpledialog.askstring(
        "Price",
        "Enter New Price"
    )
        cursor.execute(
    """
    UPDATE movies
    SET movie_name=%s,
        show_time=%s,
        ticket_price=%s
    WHERE movie_id=%s
    """,
    (
        new_name,
        new_show,
        new_price,
        movie_id
    )
)
    

    

        conn.commit()

        messagebox.showinfo(
        "Success",
        "Movie Updated Successfully"
    )

# ---------------- ADMIN - VIEW BOOKINGS ---------------- #
def view_all_bookings():
        if not is_admin():
          messagebox.showerror(
            "Access Denied",
            "Only Admin can access this feature."
        )
        return

        booking_window = tk.Toplevel(window)
        booking_window.title("All Bookings")
        booking_window.geometry("800x400")

        tree = ttk.Treeview(
        booking_window,
        columns=("ID", "USER", "MOVIE", "SEAT"),
        show="headings"
    )

        tree.heading("ID", text="Booking ID")
        tree.heading("USER", text="User ID")
        tree.heading("MOVIE", text="Movie ID")
        tree.heading("SEAT", text="Seat Number")

        tree.pack(fill="both", expand=True)

        cursor.execute("""
        SELECT booking_id,user_id,movie_id,seat_number
        FROM bookings
    """)

        for row in cursor.fetchall():
         tree.insert("", "end", values=row)
# ---------------- CANCEL TICKET ---------------- #
def cancel_ticket():

    if current_user is None:
        messagebox.showerror(
            "Login Required",
            "Please login first."
        )
        return

    booking_id = simpledialog.askstring(
        "Cancel Ticket",
        "Enter Booking ID"
    )

    if not booking_id:
        return

    # Find movie_id before deleting booking
    cursor.execute(
        """
        SELECT movie_id
        FROM bookings
        WHERE booking_id=%s
        """,
        (booking_id,)
    )

    booking = cursor.fetchone()

    if booking is None:
        messagebox.showerror(
            "Error",
            "Booking ID not found"
        )
        return

    movie_id = booking[0]

    # Increase available seats
    cursor.execute(
        """
        UPDATE movies
        SET available_seats = available_seats + 1
        WHERE movie_id=%s
        """,
        (movie_id,)
    )

    # Delete booking
    cursor.execute(
        """
        DELETE FROM bookings
        WHERE booking_id=%s
        """,
        (booking_id,)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Ticket Cancelled Successfully"
    )

# ---------------- ADMIN DASHBOARD ---------------- #
def admin_dashboard():

    if not is_admin():
        messagebox.showerror(
            "Access Denied",
            "Only Admin can access this feature."
        )
        return

    try:

        dashboard = tk.Toplevel(window)
        dashboard.title("Admin Dashboard")
        dashboard.geometry("300x200")

        cursor.execute("SELECT COUNT(*) FROM users")
        users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM movies")
        movies = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM bookings")
        bookings = cursor.fetchone()[0]

        ttk.Label(dashboard, text=f"Total Users : {users}").pack(pady=10)
        ttk.Label(dashboard, text=f"Total Movies : {movies}").pack(pady=10)
        ttk.Label(dashboard, text=f"Total Bookings : {bookings}").pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", str(e))
# ---------------- BOOKING HISTORY ---------------- #

# ---------------- BOOKING HISTORY ---------------- #

def booking_history():

    global current_user

    if current_user is None:
        messagebox.showerror(
            "Error",
            "Please Login First"
        )
        return

    user_id = current_user[0]

    history_window = tk.Toplevel(window)
    history_window.title("Booking History")
    history_window.geometry("700x400")

    cursor.execute(
        """
        SELECT booking_id,
               movie_id,
               seat_number,
               booking_date
        FROM bookings
        WHERE user_id=%s
        """,
        (user_id,)
    )

    bookings = cursor.fetchall()

    if not bookings:
        ttk.Label(
            history_window,
            text="No Bookings Found"
        ).pack(pady=20)
        return

    ttk.Label(
        history_window,
        text="BOOKING HISTORY",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    for booking in bookings:
        ttk.Label(
            history_window,
            text=f"Booking ID: {booking[0]} | Movie ID: {booking[1]} | Seat: {booking[2]} | Date: {booking[3]}"
        ).pack(pady=5)
# ---------------- SEARCH MOVIE ---------------- #
def search_movie():

    movie_name = simpledialog.askstring(
        "Search Movie",
        "Enter Movie Name"
    )

    if not movie_name:
        return

    cursor.execute("""
        SELECT movie_id,
               movie_name,
               show_time,
               available_seats,
               ticket_price
        FROM movies
        WHERE movie_name LIKE %s
    """, ("%" + movie_name + "%",))

    movies = cursor.fetchall()

    result = tk.Toplevel(window)
    result.title("Search Result")
    result.geometry("700x300")

    if not movies:
        ttk.Label(
            result,
            text="Movie Not Found"
        ).pack(pady=20)
        return

    for movie in movies:

        ttk.Label(
            result,
            text=f"ID:{movie[0]} | Movie:{movie[1]} | Show:{movie[2]} | Seats:{movie[3]} | Price:{movie[4]}"
        ).pack(pady=5)
# ---------------- LOGOUT ---------------- #
def logout():

    global current_user

    current_user = None

    welcome_label.config(text="Not Logged In")

    logout_btn.pack_forget()
    login_btn.pack(pady=8)

    add_movie_btn.pack_forget()
    delete_movie_btn.pack_forget()
    update_movie_btn.pack_forget()
    view_all_bookings_btn.pack_forget()
    admin_dashboard_btn.pack_forget()

    messagebox.showinfo(
        "Logout",
        "Logged Out Successfully"
    )
    logout_btn.pack_forget()
   
    # ---------------- TITLE ---------------- #
title = tk.Label(
# ---------------- TITLE ---------------- #

    window,
    text="🎬 MOVIE TICKET BOOKING SYSTEM",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#0f172a"
)
title.pack(pady=25)
welcome_label = tk.Label(
    window,
    text="Not Logged In",
    font=("Segoe UI", 12, "bold"),
    bg="#0f172a",
    fg="white"
)
welcome_label.pack(pady=5)

# BUTTON FRAME
button_frame = tk.Frame(
    window,
    bg="#0f172a"
)

button_frame.pack(
    fill="both",
    expand=True
)
# ---------------- BUTTONS ---------------- #
register_btn = tk.Button(button_frame, text="Register", command=register, **button_style)
register_btn.pack(pady=8)

login_btn = tk.Button(button_frame, text="Login", command=login, **button_style)
login_btn.pack(pady=8)

view_movies_btn = tk.Button(button_frame, text="View Movies", command=view_movies, **button_style)
view_movies_btn.pack(pady=8)

book_ticket_btn = tk.Button(button_frame, text="Book Ticket", command=book_ticket, **button_style)
book_ticket_btn.pack(pady=8)

booking_history_btn = tk.Button(button_frame, text="Booking History", command=booking_history, **button_style)
booking_history_btn.pack(pady=8)

add_movie_btn = tk.Button(button_frame, text="Add Movie (Admin)", command=add_movie, **button_style)

delete_movie_btn = tk.Button(button_frame, text="Delete Movie (Admin)", command=delete_movie, **button_style)

update_movie_btn = tk.Button(button_frame, text="Update Movie (Admin)", command=update_movie, **button_style)

view_all_bookings_btn = tk.Button(button_frame, text="View All Bookings", command=view_all_bookings, **button_style)

cancel_ticket_btn = tk.Button(button_frame, text="Cancel Ticket", command=cancel_ticket, **button_style)
cancel_ticket_btn.pack(pady=8)

admin_dashboard_btn = tk.Button(button_frame, text="Admin Dashboard", command=admin_dashboard, **button_style)

logout_btn = tk.Button(
    button_frame,
    text="Logout",
    command=logout,
    **button_style
)
logout_btn.pack_forget()
search_movie_btn = tk.Button(button_frame, text="Search Movie", command=search_movie, **button_style)
search_movie_btn.pack(pady=8)

exit_btn = tk.Button(button_frame, text="Exit", command=window.destroy, **button_style)
exit_btn.pack(pady=8)

window.mainloop()