import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import get_config
import html
import logging

logger = logging.getLogger(__name__)

def send_email(subject, html):
    settings = get_config()
    if settings.debug:
        logger.warn(f"mail with subject '{subject}' send triggered but email is disabled in debug mode")
        return 
    try:
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"YUH: {subject}"
        msg["From"] = settings.email_from_address
        msg["To"] = settings.email_to_address

        # Record the MIME type - text/html.
        part1 = MIMEText(html, "html")
        # Attach parts into message container
        msg.attach(part1)

        # Credentials
        username = settings.email_from_address
        password = settings.email_password

        # Sending the email
        ## note - this smtp config worked for me, I found it googling around, you may have to tweak the # (587) to get yours to work
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(settings.email_from_address, settings.email_to_address, msg.as_string())
        server.quit()
    except Exception as ex:
        logging.exception(f"error sending email")

def format_last_exception(escape=1):
    import traceback, sys

    limit = None
    type, value, tb = sys.exc_info()
    list = traceback.format_tb(tb, limit
        ) + traceback.format_exception_only(type, value)
    body = "Traceback (innermost last):\n" + "%-20s %s" % (
        "".join(list[:-1]), list[-1] )
    if escape:
        body = '\n<PRE>'+html.escape(body)+'</PRE>\n'
    return body
