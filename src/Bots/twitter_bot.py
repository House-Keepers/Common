import json

import os
import re
import tweepy


class TwitterBot(BaseBot):
    def parse_format(self, **kwargs):
        pass

    def __init__(self, sender_email, password):
        super().__init__()
        self.sender_email = sender_email
        self.message = None
        self.encoding = "utf-8"
        self.password = password
        self.mail_to_send = None
        self.mailer = self.login(sender_email, password)

    def login(self, sender_email, password):
        return Mailer(smtp_server=self.sender_email, smtp_user='me', smtp_port=587, smtp_password=password,
                      security='tls', debug=True)

    def parse_format_smtp(self, subject: str, body: str, receiver_email: str, attachment=None, file_name=None):
        # Create a multipart message and set headers
        self.message = MIMEMultipart("alternative")
        self.message["From"] = self.sender_email
        self.message["To"] = receiver_email
        self.message["Date"] = formatdate(localtime=False)
        self.message["LocalDate"] = formatdate(localtime=True)
        self.message["Message-Id"] = make_msgid()
        self.message["Subject"] = Header(subject, self.encoding)
        self.message["Subject"] = subject
        self.message["Bcc"] = receiver_email  # Recommended for mass emails
        # Add body to email
        self.message.attach(MIMEText(body, "plain", self.encoding))
        if attachment:
            self.add_atachment(attachment, file_name)
        return self.message.as_string()

    def add_atachment(self, attachment, filename: str, ):
        att_filename = filename
        if isinstance(attachment, bytes):
            # Let's suppose we directly attach binary data
            payload = attachment
        else:
            with open(attachment, "rb") as f_attachment:
                payload = f_attachment.read()
                if not filename:
                    att_filename = os.path.basename(attachment)
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(payload)

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            "attachment; filename=%s" % att_filename,
        )

        # Add attachment to message and convert message to string
        self.message.attach(part)

    def run2(self, subject: str, body: str, recipients: list, attachment=None, file_name=None,
             split_mails=True):
        # Log in to server using secure context and send email
        rfc822_addresses = self.get_recipient_mails(recipients)
        if rfc822_addresses:
            result = True
            if split_mails:
                for recipient in rfc822_addresses:
                    _result = self._send_email(subject, body, recipient, attachment, file_name)
                    if not _result:
                        result = _result
            else:
                recipient = ", ".join(rfc822_addresses)
                result = self._send_email(subject, body, recipient, attachment, file_name)
            return result

    def _send_email(self, subject: str, body: str, receiver_email: str, attachment=None, file_name=None):
        try:
            # Log in to server using secure context and send email
            mail_to_send = self.parse_format_smtp(subject, body, attachment, file_name)
            context = ssl.create_default_context()
            with smtplib.SMTP("localhost", 587) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, receiver_email, mail_to_send)
                return True

        except (
                smtplib.SMTPAuthenticationError,
                smtplib.SMTPSenderRefused,
                smtplib.SMTPRecipientsRefused,
                smtplib.SMTPDataError,
                ConnectionRefusedError,
                ConnectionAbortedError,
                ConnectionResetError,
                ConnectionError,
                ssl.SSLError
        ) as exc:
            print("Cannot send email: %s", exc)
            return False

    @staticmethod
    def is_mail_address(mail: str):
        """
        Check email address validity against simpler than RFC822 regex
        """
        if re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9][a-zA-Z0-9]+$", mail):
            return True
        return False

    def get_recipient_mails(self, recipient_mails):
        if not isinstance(recipient_mails, list):
            # Make sure destination mails is a list
            recipient_mails = re.split(r",|;| ", recipient_mails)
        # Strip extra chars around mail addresses
        recipient_mails = [mail.strip() for mail in recipient_mails]
        rfc822_addresses = [mail for mail in recipient_mails if self.is_mail_address(mail)]
        non_rfc822_addresses = [
            mail for mail in recipient_mails if mail not in rfc822_addresses
        ]
        if not non_rfc822_addresses == []:
            print("Refused non RFC 822 mails: %s", format(non_rfc822_addresses))
            return False
        return recipient_mails

    def run(self, subject: str, body: str, recipients: list, attachment=None, file_name=None,
            split_mails=True):
        """"
        :param subject: the mail subject
        :param body: the mail body
        :param recipients: the receivers email
        :param attachment : attachment can be a binary blob or a file path
        :param file_name : filename is optional, and will rename a binary blob to something more meaningful
        :param split_mails: split_mails=True will send one email per recipient,
        split_mails=False will send one email for all recipients
        """
        mailer = Mailer(smtp_server=self.sender_email, smtp_user='me', smtp_port=465, smtp_password="ig214000",
                        security='ssl', debug=False)
        if attachment and file_name:
            mailer.send_email(subject=subject, sender_mail=self.sender_email, recipient_mails=recipients,
                              body=body, split_mails=split_mails, attachment=attachment, filename=file_name)
        else:
            mailer.send_email(subject=subject, sender_mail=self.sender_email, recipient_mails=recipients,
                              body=body, split_mails=split_mails)


m = MailBot("igafni9@gmail.com", "ig214000")
m.run2(subject="בדיקה", body="אוהב אותך", recipients=["igafni@proton.me"])
# import yagmail
#
# receiver = "igafni@proton.me"
# body = "Hello there from Yagmail"
# filename = "document.pdf"
#
# yag = yagmail.SMTP("igafni@proton.me", password="Ig214000")
# yag.send(
#     to=receiver,
#     subject="Yagmail test with attachment",
#     contents=body
# )
