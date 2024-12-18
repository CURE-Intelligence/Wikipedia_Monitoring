import smtplib
from email.mime.text import MIMEText
from typing import Dict

def send_email(subject: str, 
               body: str, 
               credentials: Dict[str, str],
               to_technical:bool = True):
    """
        Send an email notification with the specified subject and body.
    
        This function composes and sends an email using the Simple Mail Transfer Protocol (SMTP). 
        The email can be directed either to a technical team or to a general user based on 
        the `to_technical` flag.
    
        Args:
            subject (str): 
                The subject line of the email. It will be prefixed with 'CURE Notification:' 
                to indicate the source of the notification.
            
            body (str): 
                The main content of the email. This can be plain text or HTML-formatted text, 
                depending on the requirements of the recipients.
            
            to_technical (bool, optional): 
                A flag to determine the recipient group of the email.
                - If `True`, the email is sent to the technical team (`TO_TECH_EMAIL`).
                - If `False` (default), the email is sent to the general user (`TO_USER_EMAIL`).
    
        Raises:
            smtplib.SMTPException: 
                If an error occurs during the SMTP connection, authentication, or while sending the email.
            
            Exception: 
                For any other unforeseen errors that may arise during the email composition or sending process.

    """
    # Create the MIMEText object with the email body (Formatting the email body and subject)
    
   
    print(f"Sending email with subject: {subject}")
    print(f"Body: {body}")
    
    message = MIMEText(body)
    message['Subject'] = subject
    #message['From'] = FROM_EMAIL
    message['From'] = credentials['FROM_EMAIL']
    #message['To'] = TO_TECH_EMAIL if to_technical else TO_USER_EMAIL
    message['To'] = credentials['TO_TECH_EMAIL'] if to_technical else credentials['TO_USER_EMAIL']
        
    # Connect to Server
    #server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server = smtplib.SMTP(credentials['SMTP_SERVER'], credentials['SMTP_PORT'])
    #server.connect()
        
    server.ehlo()    
    server.starttls()
    
    # Login to the server and send the email
    server.login(credentials['SMTP_USERNAME'],
                 credentials['SMTP_PASSWORD'])
    
    server.sendmail(credentials['FROM_EMAIL'],
                    credentials['TO_TECH_EMAIL'],
                    message.as_string()
                    )
    
    #server.login(SMTP_USERNAME, SMTP_PASSWORD)
    #server.sendmail(FROM_EMAIL, TO_TECH_EMAIL, message.as_string())
        
    server.quit()