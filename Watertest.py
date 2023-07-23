import smtplib
import time
import datetime

from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BaseCase.main(__name__, __file__)

BASEURL = "https://monitormywatershed.org/sites/MSPL2S/"
FIVE_MINUTES = 5
DELTA = [1000, 26, 600, 150, 1000, 40, 5, 100, 100]
Name = ["Water depth", "Temperature", "Electrical Conductivity", "Turbidity", "Turbidity", "Temperature", "Battery Voltage", "Percent Full Scale", "Relative Humidity"]

# Your Gmail account and app password
GMAIL_USER = 'tricarico001@gmail.com'
GMAIL_PASSWORD = 'ipfvvkgxiwhzdkcy'

# List of recipients
EMAIL_RECIPIENTS = ['tricarico1@epix.net']

def send_email(subject, body):
    message = f'Subject: {subject}\n\n{body}'
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, EMAIL_RECIPIENTS, message)
    except Exception as e:
        print(f"Error sending email: {e}")

class TestMFALogin(BaseCase):
    last_email_sent = -1

    def test_mfa_login(self):
        while(True):
            self.open(BASEURL)
            time.sleep(5)

            values = []
            n = 9

            for i in range(1, n+1):
                time.sleep(2)
                value_css_selector = f"div.mdl-dialog__content > div > table:nth-child({i}) tbody tr:nth-last-child(1) td:nth-last-child(1)"
                value = float(self.get_text_content(value_css_selector))
                values.append(value)

                print("values", values)

                value = values[i-1]

                difference = 0

                if self.last_email_sent == -1:
                    if value >= DELTA[i-1] or value < 0:
                        send_email(f"{Name[i-1]} Alert", f"{Name[i-1]} has reached {value}.")
                        self.last_email_sent = datetime.datetime.utcnow()
                else:
                    difference = datetime.datetime.utcnow() - self.last_email_sent
                    if difference.total_seconds() >= 3600 * 24 and (value >= DELTA[i-1] or value < 0):
                        send_email(f"{Name[i-1]} Alert", f"{Name[i-1]} has reached {value}.")
                        self.last_email_sent = datetime.datetime.utcnow()

            time.sleep(FIVE_MINUTES)
