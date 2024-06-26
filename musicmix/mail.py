import smtplib
from email.message import EmailMessage
from django.conf import settings

class Email:
    def __init__(self, subject: str, receipient: str, contents: str) -> None:
        self.subject = subject
        self.receipient = receipient
        self.contents = contents
    
    def _init_message(self):
        self.message = EmailMessage()
        self.message['Subject'] = self.subject
        self.message['To'] = self.receipient
        self.message.set_content(self.contents)

class EmailSender:
    def __init__(self):
        self.hostname = settings.EMAIL_HOST
        self.client = smtplib.SMTP_SSL(self.hostname, 587)
        # TODO moet ik ervoor zorgen dat de login aan blijft staan?
        self._login_and_init()
    def _login_and_init(self):
        self.client.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        self.client.starttls()
        self.client.ehlo()
    def send(self, email: Email):
        self.client.send_message(email.message)
        