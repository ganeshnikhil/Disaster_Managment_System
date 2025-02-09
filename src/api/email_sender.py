# import smtplib, ssl
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from src.Parser.Compont import generate_html_report
# from Data.Const.constants import CITY_EMAILS
# from dotenv import load_dotenv
# from os.path import exists
# from os import getenv
# from src.File.json_op import read_json_file , search_zip
# import logging 


# load_dotenv()
# CACHED_RESPONSE_PATH = "./Data/Cache/zip_report_cache.json"
# email_password = getenv("email_password")
# sender_email = getenv("sender_email")
# def send_email(html_content , password, sender_email , receiver_email , smtp_server="smtp.gmail.com", port=587):
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = "DISASTER UPDATE"
        
#         msg.attach(MIMEText(html_content, 'html'))
        
#         context = ssl.create_default_context()
#         with smtplib.SMTP(smtp_server, port) as server:
#             server.ehlo()  # Can be omitted
#             server.starttls()
#             server.ehlo()  # Can be omitted
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#             print(f"Email send succesfully to {receiver_email}")
#             return True 
#     except Exception as e:
#         print(f"Error: {e}")
#     return False 


# def integrated_email(zipcode):
#     if not exists(CACHED_RESPONSE_PATH):
#         logging.error("JSON file path does not exist.")
#         return None
    
#     response = search_zip(zipcode, CACHED_RESPONSE_PATH)
    
#     if response:
#         logging.info("The report is found, setting up email.")
#         city_name = response.get("city", "Local")  # Default to "Local" if city_name is None
#         receiver_email = CITY_EMAILS.get(city_name, CITY_EMAILS["Local"])  # Fallback to "Local"

#         html_report = generate_html_report(response)
#         send_email(html_report, email_password, sender_email, receiver_email)
#         logging.info(f"Report sent to {receiver_email}.")

#         return True
    
#     return False


import smtplib
import ssl
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.Parser.Compont import generate_html_report
from Data.Const.constants import CITY_EMAILS
from dotenv import load_dotenv
from os.path import exists
from os import getenv
from src.File.json_op import search_zip

# Load environment variables
load_dotenv()

# Constants
CACHED_RESPONSE_PATH = "./Data/Cache/zip_report_cache.json"
SMTP_SERVER = getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(getenv("SMTP_PORT", 587))
email_password = getenv("email_Password")
sender_email = getenv("Sender_email")

def send_email(html_content, password, sender_email, receiver_email, smtp_server=SMTP_SERVER, port=SMTP_PORT):
    """Send an email with disaster updates."""
    if not password or not sender_email:
        logging.error("Email credentials are missing. Check environment variables.")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "DISASTER UPDATE"
        msg.attach(MIMEText(html_content, 'html'))

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)  # Upgrade connection to secure TLS
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True 

    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication failed. Check email/password.")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while sending email: {e}")

    return False 

def integrated_email(zipcode , direct = False):
    """Fetches the disaster report and sends an email."""
    
    if not exists(CACHED_RESPONSE_PATH):
        logging.error("JSON file path does not exist.")
        return False
    response = search_zip(zipcode, CACHED_RESPONSE_PATH)
    if response:
        logging.info("Report found, setting up email.")
        city_name = response.get("city", "Local")
        receiver_email = CITY_EMAILS.get(city_name, CITY_EMAILS["Local"])

        html_report = generate_html_report(response)
        if send_email(html_report, email_password, sender_email, receiver_email):
            logging.info(f"Report successfully sent to {receiver_email}.")
            return True

    return False

def direct_email(response):
    city_name = response.get("city", "Local")
    receiver_email = CITY_EMAILS.get(city_name, CITY_EMAILS["Local"])
    receiver_email = "ganeshnikhil124@gmail.com"
    html_report = generate_html_report(response)
    if send_email(html_report, email_password, sender_email, receiver_email):
        logging.info(f"Report successfully sent to {receiver_email}.")
        return True