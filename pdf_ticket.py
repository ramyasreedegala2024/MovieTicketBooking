from reportlab.pdfgen import canvas


def generate_ticket(movie_name, seat, user_name):

    filename = f"{user_name}_ticket.pdf"

    pdf = canvas.Canvas(filename)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, 800, "MOVIE TICKET")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 740, f"User Name : {user_name}")
    pdf.drawString(100, 710, f"Movie Name : {movie_name}")
    pdf.drawString(100, 680, f"Seat Number : {seat}")

    pdf.save()

    print("PDF Ticket Generated:", filename)