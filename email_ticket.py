import smtplib
from email.message import EmailMessage

def send_ticket(receiver_email, movie_name, seat):

    sender_email = "yourgmail@gmail.com"
    app_password = "your_app_password"

    msg = EmailMessage()

    msg["Subject"] = "Movie Ticket Confirmation"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(
        f"""
Movie Ticket Booked Successfully

Movie : {movie_name}
Seat  : {seat}

Thank You!
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)