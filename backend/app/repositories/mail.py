from email.message import EmailMessage
import aiosmtplib
from backend.app.core.config import settings
from backend.app.core.log import get_logger
import ssl

logger = get_logger(__file__)


class Email:
    def __init__(self):
        self.settings = settings

    async def __call__(self, receiver_email: str, subject: str, body: str) -> bool:
        for i in range(1, 4):
            try:
                message = EmailMessage()
                message["Subject"] = subject
                message["From"] = settings.SMTP_USER
                message["To"] = receiver_email

                message.set_content(body)
                tls_context = ssl.create_default_context()
                tls_context.check_hostname = False
                tls_context.verify_mode = ssl.CERT_NONE

                current_port = int(settings.SMTP_PORT)
                is_port_465 = current_port == 465

                await aiosmtplib.send(
                    message,
                    hostname=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    username=settings.SMTP_USER,
                    password=settings.SMTP_PASSWORD,
                    use_tls=is_port_465,
                    start_tls=not is_port_465,
                    tls_context=tls_context
                )
                return True
            except Exception as e:
                logger.error(f"(Try:{i}) Error sending mail to {receiver_email}: {e}")

        logger.error(f"Failed to send messages to {receiver_email}")
        return False
