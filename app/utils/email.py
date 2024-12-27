# utils/email.py
from flask_mail import Message
from flask_mail import Mail

mail = Mail() 


def send_email(subject,recipients,body,sender="hemorafriqa@gmail.com"):
    message = Message(
        subject,
        recipients=recipients,
        body=body,
        sender=sender
        )
    mail.send(message)
