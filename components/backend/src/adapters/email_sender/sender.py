from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import Optional, List

from pydantic import validate_arguments
from dataclasses import dataclass, field

from .serializer import Serializer
from src.application import services
from src.application.dto import Event

@dataclass
class BaseMailSender:
    smtp_sender: str
    smtp_password: str
    smtp_host: str
    smtp_port: int
    session: Optional[SMTP] = field(default=None, init=False)

    def update_session(self):
        self.session = SMTP(self.smtp_host, self.smtp_port)
        self.session.ehlo()
        self.session.starttls()
        self.session.login(self.smtp_sender, self.smtp_password)

@dataclass
class NotificationMailSender(BaseMailSender):
    def __check_connection(self):
        if not self.session:
            self.update_session()
        else:
            try:
                self.session.ehlo()
            except Exception:
                self.update_session()

    @validate_arguments
    def send_event(self, email_message: Event, emails: List[str]):
        self.__check_connection()
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Subject'
        message['From'] = self.smtp_sender

        html = Serializer.serialize_event(email_message)
        message.attach(MIMEText(html, 'html'))

        for email in emails:
            message['To'] = email
            self.session.send_message(message, self.smtp_sender, email)