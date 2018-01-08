import smtplib
from app.conf.config import gmail_user, gmail_password
from email.mime.text import MIMEText
from email.header import Header
from app import logger

class mail:
    def __init__(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(gmail_user, gmail_password)
        logger.info("success connected")
        self.me = "smart_park"

    def send(self, to, subject, message):
        msg = MIMEText(message, 'html', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = Header(self.me, 'utf-8')
        msg['To'] = Header(to, 'utf-8')
        try:
            self.server.sendmail(self.me, to, msg.as_string())
            logger.info("Email sent receiver: {}".format(to))
        except smtplib.SMTPException as e:
            self.server.ehlo()
            self.server.login(gmail_user, gmail_password)
            logger.error(e)
