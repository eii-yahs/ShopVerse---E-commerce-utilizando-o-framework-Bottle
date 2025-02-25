import smtplib
from email.mime.text import MIMEText

# Classe de envio de e-mails
class EmailService:
    SENDER_EMAIL = ""
    SENDER_PASSWORD = ""
    @staticmethod
    def send_email(to_email, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EmailService.SENDER_EMAIL
        msg['To'] = to_email

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EmailService.SENDER_EMAIL, EmailService.SENDER_PASSWORD)
            server.sendmail(EmailService.SENDER_EMAIL, to_email, msg.as_string())
            server.quit()
            print("E-mail enviado com sucesso!")
            return True
        except smtplib.SMTPAuthenticationError:
            print("Erro de autenticação. Verifique sua senha de aplicativo.")
        except smtplib.SMTPConnectError:
            print("Erro ao conectar ao servidor SMTP. Tente novamente.")
        except smtplib.SMTPException as e:
            print(f"Erro ao enviar e-mail: {e}")
        return False