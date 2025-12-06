import logging

from asgiref.sync import async_to_sync
from celery import Celery
from backend.src.utils.mail import generate_reset_password_email, mail
from backend.src.core.config import settings

logger = logging.getLogger(__name__)

celery_app = Celery()
celery_app.conf.update(
    broker_url=settings.redis_url,
    result_backend=settings.redis_url
)

@celery_app.task()
def send_password_reset_email(recipient: str, code: str):
    logger.info(f"Task started: Sending password reset email to {recipient} with code {code}")
    try:
        # Генерация сообщения
        message = generate_reset_password_email([recipient], code)
        logger.info(f"Message generated: {message}")

        # Синхронная отправка почты
        async_to_sync(mail.send_message)(message)
        print("Email sent")

        logger.info(f"Email successfully sent to {recipient}")

    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {str(e)}")
        raise e