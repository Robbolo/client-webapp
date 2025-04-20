from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import black
from django.conf import settings
from pathlib import Path
from datetime import date
import os

# Load .env file (this should only run once)


def generate_invoice_pdf(buffer, client_name, client_email, package_info, session_price, total_price, due_date):

    # Load font and logo paths
    reg_font_path = Path(settings.BASE_DIR) / 'clients' / 'utils' / 'Alegreya-Regular.ttf'
    bold_font_path = Path(settings.BASE_DIR) / 'clients' / 'utils' / 'Alegreya-Bold.ttf'
    italic_font_path = Path(settings.BASE_DIR) / 'clients' / 'utils' / 'Alegreya-Italic.ttf'
    logo_path = Path(settings.BASE_DIR) / 'clients' / 'utils' / 'logo.png'

    # Register font
    pdfmetrics.registerFont(TTFont('Alegreya', str(reg_font_path)))
    pdfmetrics.registerFont(TTFont('Alegreya-Bold', str(bold_font_path)))
    pdfmetrics.registerFont(TTFont('Alegreya-Italic', str(italic_font_path)))

    # Create canvas
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Alegreya", 12)
    c.setFillColor(black)

    margin = 20 * mm
    line_height = 16
    y = height - 40 * mm  # Start near top

    # Logo (top left)
    c.drawImage(str(logo_path), margin, y-120, width=60*mm, preserveAspectRatio=True, mask='auto')
    
    # Today's date under the logo
    today = date.today().strftime("%d %B %Y")
    c.drawString(margin, y - 120, today)

    # Friend's info (top right)
    right_x = width - margin
    info_y = height - 40 * mm

    #set details from dotenv
    name = os.environ.get("NAME", "Coaching Services")
    insta = os.environ.get("INSTA", "Unknown Insta")
    email = os.environ.get("EMAIL", "Unknown Email")
    website = os.environ.get("WEBSITE", "Unknown Website")


    # First line: Bold
    c.setFont("Alegreya-Bold", 12)
    c.drawRightString(right_x, info_y, f"{name}")

    # Second line: Italic
    c.setFont("Alegreya-Italic", 11)
    c.drawRightString(right_x, info_y - line_height, "Neurodiversity Coach, Speaker & Consultant")

    # Third and fourth: Regular
    c.setFont("Alegreya", 12)
    c.drawRightString(right_x, info_y - line_height * 2, f"{insta}")
    c.drawRightString(right_x, info_y - line_height * 3, f"{email}")
    c.drawRightString(right_x, info_y - line_height * 4, f"{website}")

        # Spacer
    y = y - 150

    # Letter body
    c.setFont("Alegreya", 12)
    first_name = client_name.split(' ')[0]
    c.drawString(margin, y, f"FAO: {client_name},")
    y -= line_height
    c.drawString(margin, y, f"{client_email}")
    y -= line_height * 1.5
    y -= 20
    text_object = c.beginText(margin, y)
    text_object.setFont("Alegreya", 12)
    text_object.textLines(f"Dear {first_name},\n\n"
                      "I look forward to working with you and making our way together "
                      "towards your goals! \n Please see below for payment totals and schedule.")
    c.drawText(text_object)

# Adjust y for spacing after the text block
    y = text_object.getY() - 10

    y -= line_height * 1.5

    # Section: Fee payment / Schedule
    c.setFont("Alegreya-Bold", 13)
    header_text = "Fee payment / Schedule"
    c.drawString(margin, y, header_text)
    text_width = pdfmetrics.stringWidth(header_text, "Alegreya", 13)
    c.line(margin, y - 2, margin + text_width, y - 2)
    y -= line_height * 1.2

    c.setFont("Alegreya", 12)
    c.drawString(margin, y, "Payment is due by:")
    c.setFont("Alegreya-Bold", 12)
    c.drawString(margin + 100, y, due_date.strftime('%d %B %Y'))
    y -= line_height * 2

    # Section: Services and Discounts
    c.setFont("Alegreya-Bold", 13)
    header_text = "Services and Discounts"
    text_width = pdfmetrics.stringWidth(header_text, "Alegreya-Bold", 13)
    c.drawString(margin, y, "Services and Discounts")
    c.line(margin, y - 2, margin + text_width, y - 2)
    y -= line_height * 1.5

    c.setFont("Alegreya", 12)
    c.drawString(margin, y, f"1 x Coaching Package: {package_info}")
    y -= line_height
    c.drawString(margin + 20, y, f"Coaching services @ £{session_price:.2f} GBP per session")
    y -= line_height * 2

    c.setFont("Alegreya-Bold", 12)
    c.setFillColor(black)
    c.setFont("Alegreya-Bold", 13)
    header_text = f"TOTAL £{total_price:.2f} GBP"
    text_width = pdfmetrics.stringWidth(header_text, "Alegreya-Bold", 13)
    c.drawString(margin, y, header_text)
    c.line(margin, y - 2, margin + text_width, y - 2)
    y -= line_height * 2

    # Section: Payment Info

    c.setFont("Alegreya", 12)
    c.drawString(margin, y, "Please make payment to the account below with your ")
    c.setFont("Alegreya-Bold", 12)
    c.drawString(margin + 260, y, "first name and last initial as a reference")
    y -= line_height * 2

    bank_name = os.environ.get("BANK_NAME", "Unknown Bank")
    account_name = os.environ.get("BANK_ACCOUNT_NAME", "Jane Doe")
    account_number = os.environ.get("BANK_NUMBER", "00000000")
    sort_code = os.environ.get("BANK_SORT_CODE", "00-00-00")
    bic = os.environ.get("BIC", "Unknown BIC")
    iban = os.environ.get("IBAN", "Unknown IBAN")

    c.setFont("Alegreya", 12)
    c.drawString(margin, y, f"Name: {account_name}")
    y -= line_height
    c.drawString(margin, y, f"Bank: {bank_name}")
    y -= line_height
    c.drawString(margin, y, f"Account Number: {account_number}")
    y -= line_height
    c.drawString(margin, y, f"Sort Code: {sort_code}")
    y -= line_height
    c.drawString(margin, y, f"BIC: {bic}")
    y -= line_height
    c.drawString(margin, y, f"IBAN: {iban}")
    y -= line_height * 2

    c.setFont("Alegreya", 12)
    c.drawString(margin, y, "Please do not hesitate to contact me if you have any questions.")

    # Finish
    c.showPage()
    c.save()
