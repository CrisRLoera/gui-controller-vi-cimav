from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class EmailController:
    def __init__(self,host):
        self.host = host
        self.email_host = self.host.file_controller.conf_file["host"]
        self.port = self.host.file_controller.conf_file["port"]

    def send_interruption_email(self,program_owner):
        mailtext = "There has been an interruption in your program. Now is been restored and started."
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Program interruption"
        msg['From'] = self.host.file_controller.conf_file["sender"]
        msg['To'] = program_owner
        # To create plain text mails
        part= MIMEText(mailtext, 'plain')
        msg.attach(part)
        
        server = smtplib.SMTP(self.email_host,self.port)
        try:
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        except:
            print("No send email interruption")
        server.quit()

    def send_step_change_email(self,program_owner,step_type,step_number):
        mailtext = f"The step {step_type}-{step_number} has been completed sucesfully."
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Step change"
        msg['From'] = self.host.file_controller.conf_file["sender"]
        msg['To'] = program_owner
        # To create plain text mails
        part= MIMEText(mailtext, 'plain')
        msg.attach(part)
        
        server = smtplib.SMTP(self.email_host,self.port)
        try:
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        except:
            print("No send email interruption")
        server.quit()

# mandar correo al finalizar
    def send_program_finalize_email(self,program_owner,end_message):
        mailtext = f"The program has ended with completion status - {end_message}."
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Program completed"
        msg['From'] = self.host.file_controller.conf_file["sender"]
        msg['To'] = program_owner
        # To create plain text mails
        part= MIMEText(mailtext, 'plain')
        msg.attach(part)
        
        server = smtplib.SMTP(self.email_host,self.port)
        try:
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        except:
            print("No send email interruption")
        server.quit()


# mandar correo cuando se requiere manteniminetos
    def send_maintenance_email(self,maintenance,part):
        # Change the message
        mailtext = f"The {part} requires inspection and maintenance."
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"{part} maintenance"
        msg['From'] = self.host.file_controller.conf_file["maintenance"]
        msg['To'] = maintenance
        # To create plain text mails
        part= MIMEText(mailtext, 'plain')
        msg.attach(part)
        
        server = smtplib.SMTP(self.email_host,self.port)
        try:
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        except:
            print("No send email interruption")
        server.quit()





