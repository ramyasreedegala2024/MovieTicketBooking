from database import *

def register():

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    if cursor.fetchone():
        print("Email Already Exists!")
        return

    cursor.execute(
        """
        INSERT INTO users(name,email,password)
        VALUES(%s,%s,%s)
        """,
        (name,email,password)
    )

    conn.commit()

    print("Registration Successful!")


def login():

    email = input("Enter Email: ")
    password = input("Enter Password: ")

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """,
        (email,password)
    )

    user = cursor.fetchone()

    if user:
        print("Login Successful!")
        print("Welcome", user[1])
    else:
        print("Invalid Email or Password")


def change_password():

    email = input("Enter Email: ")
    old_password = input("Enter Old Password: ")

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """,
        (email,old_password)
    )

    user = cursor.fetchone()

    if not user:
        print("Invalid Credentials!")
        return

    new_password = input("Enter New Password: ")

    cursor.execute(
        """
        UPDATE users
        SET password=%s
        WHERE email=%s
        """,
        (new_password,email)
    )

    conn.commit()

    print("Password Changed Successfully!")


def forgot_password():

    email = input("Enter Email: ")

    cursor.execute(
        "SELECT password FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if user:
        print("Your Password is:", user[0])
    else:
        print("Email Not Found!")