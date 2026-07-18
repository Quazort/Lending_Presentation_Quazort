import ssl
import logging
import asyncio
import aiosmtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)


class Email:
    def __init__(self, settings):
        self.settings = settings

    async def __call__(self, receiver_email: str, subject: str, body: str) -> bool:
        tls_context = ssl.create_default_context()
        tls_context.check_hostname = False
        tls_context.verify_mode = ssl.CERT_NONE

        for i in range(1, 4):
            try:
                message = EmailMessage()
                message["Subject"] = subject
                message["From"] = self.settings.SMTP_USER
                message["To"] = receiver_email

                message.set_content(body)

                port = int(self.settings.SMTP_PORT)

                await aiosmtplib.send(
                    message,
                    hostname=self.settings.SMTP_HOST,
                    port=port,
                    username=self.settings.SMTP_USER,
                    password=self.settings.SMTP_PASSWORD,
                    use_tls=(port == 465),
                    start_tls=(port != 465),
                    tls_context=tls_context,
                    timeout=10
                )
                logger.info(f"Email successfully sent to {receiver_email}")
                return True
            except Exception as e:
                logger.error(f"(Try:{i}) Error sending mail to {receiver_email}: {e}")
                await asyncio.sleep(1)

        return False