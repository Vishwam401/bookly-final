from celery import Celery
from src.mail import mail, create_message
from asgiref.sync import async_to_sync
from src.config import Config

c_app = Celery("tasks") # Task name de do

c_app.config_from_object('src.config')

# Render Redis SSL Fix: Ye settings compulsory hain
c_app.conf.update(
    broker_use_ssl={
        'ssl_cert_reqs': 'none'
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': 'none'
    }
)

@c_app.task()
def send_email(recipients: list[str], subject: str , body : str):
    message = create_message(
        recipient=recipients,
        subject=subject,
        body=body,
    )

    # FastAPI-Mail async hai, isliye async_to_sync sahi hai
    async_to_sync(mail.send_message)(message)
    print("Email sent successfully!")