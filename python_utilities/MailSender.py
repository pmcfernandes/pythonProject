from smtplib import SMTPException, SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import ssl


class MailSender:
    def __init__(self, sender: str, to: list, subject: str):
        self.__from = sender
        self.__to = to
        self.__subject = subject
        self.__message = ""
        self.__username = ""
        self.__password = ""
        pass

    def getContentType(self):
        match = re.search("</?\s*[a-z-][^>]*\s*>|(\&(?:[\w\d]+|#\d+|#x[a-f\d]+);)", self.__message)
        return "html" if match else "plain"

    def setMessage(self, content: str):
        self.__message = content
        pass

    def setUsername(self, username: str):
        self.__username = username
        pass

    def setPassword(self, password: str):
        self.__password = password
        pass

    def send(self, host: str = "localhost", port: int = 25) -> bool:
        msg = MIMEMultipart()
        msg['From'] = self.__from
        msg['To'] = ", ".join(self.__to)
        msg['Subject'] = self.__subject
        msg.attach(MIMEText(self.__message, self.getContentType(), "utf-8"))

        context = ssl.create_default_context()

        try:
            smtp = SMTP(host, port)
            smtp.ehlo()
            if port == 587:
                smtp.starttls(context=context)
                smtp.ehlo()

            if len(self.__username) > 0 and len(self.__password) > 0:
                smtp.login(self.__username, self.__password)

            smtp.sendmail(self.__from, self.__to, msg.as_string())
        except SMTPException as e:
            print(e)
            return False
        finally:
            smtp.quit()
        return True

