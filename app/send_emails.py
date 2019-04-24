import smtplib

import config
from app.models import Book, Meta_book



def send_email(receiver,topic,book_id):
    metabook_id = Book.query.filter_by(id=book_id).first().metabook_id
    name = Meta_book.query.filter_by(id=metabook_id).first().name
    if topic == "remind":
        subject = "Reminder to return Book"
        msg = "This is a reminder that you should return {} in the next 24 hours.".format(name)
    
    elif topic == "requested":
        subject = "Succesful book request"
        msg = "You have succesfully requested {}.".format(name)
    
    elif topic == "requesting":
        subject = "Book requested"
        msg = "Someone has requested {} from you.".format(name)

    else:
        raise TypeError("The topic wasn't in the options available.")
        return
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