# utils/email.py
from flask_mail import Message
from app import mail 


def send_email(subject,recipients,body,sender="hemorafriqa@gmail.com"):
    message = Message(
        subject,
        recipients=recipients,
        body=body,
        sender=sender
        )
    mail.send(message)
