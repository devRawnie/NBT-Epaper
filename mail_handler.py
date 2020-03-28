import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

def send(to_email, subject, link):
    content = '<a href="{link}"><button style="background-color: #000000;color:white;border-radius:2px;">Daily NBT</button></a>'.format(link=link)
    subject = datetime.now().strftime("NBT Newspaper - %d %B %Y")
    print("Status: Preparing Mail")
    message = Mail(
        from_email='rohitsdec4@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=content)
    try:
        print("Status: Mail Prepared")
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print("Status: Mail sent successfully to '%s'" % to_email)
    except Exception as e:
        print(e.message)
        return False
    
    return True