import smtplib

import config


def send_email(receiver,subject,msg):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(config.EMAIL, config.PASSWORD)
        message = "Subject: {}\n\n{}".format(subject,msg)
        server.sendmail(config.EMAIL,receiver,message)
        server.close()
        print("Email sent!")
    except:
    	print("Email failed to send.")

subject = "Hi"
msg = "What's up"

send_email(config.EMAIL,subject,msg)