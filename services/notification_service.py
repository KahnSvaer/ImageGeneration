import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class EmailNotificationSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.username = os.getenv("SENDER_EMAIL")
        self.password = os.getenv("SENDER_PASSWORD")

    def send_email(self, to_email, image_link):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = "Your Content has been generated"

            message = f"Hello your content has been generated. Please enter {image_link} link to view your content. Thank you for using our services"
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()  # Secure the connection
                server.login(self.username, self.password)
                server.sendmail(self.username, to_email, msg.as_string())

        except Exception as e:
            print(f"Failed to send email: {e}")


if __name__ == "__main__":
    username = os.getenv("SENDER_EMAIL")
    sender = EmailNotificationSender()
    sender.send_email(
        to_email=username,
        image_link = ""
    )
