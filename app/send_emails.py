import smtplib

from app import config
from app.models import User, Meta_book, Book, Transaction
from datetime import datetime, date, timedelta



def send_email(receiver,topic,book_id):
    metabook_id = Book.query.filter_by(id=book_id).first().metabook_id
    name = Meta_book.query.filter_by(id=metabook_id).first().name
    if topic == "remind":
        subject = "Reminder to return Book"
        msg = "This is a reminder that you should return {} in the next 24 hours.".format(name)
    
    elif topic == "requested":
        subject = "Successful book request"
        msg = "You have successfully requested {}.".format(name)
    
    elif topic == "requesting":
        subject = "Book requested"
        msg = "Someone has requested {} from you.".format(name)

    elif topic == "reject1":
        subject = "Request denied"
        msg = "Unfortunately, your petition for {} was rejected.".format(name)
    
    elif topic == "reject2":
        subject = "Rejected book request"
        msg = "You have successfully rejected a request for {}.".format(name)

    elif topic == "l_confirm1":
        subject = "Book lending confirmed"
        msg = "Your request for {} has been approved.".format(name)

    elif topic == "l_confirm2":
        subject = "Book lending confirmed"
        msg = "You have confirmed to lend {}.".format(name)

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

def remind_return():
    transactionsQ = Transaction.query.filter_by(status='borrower_confirmed',enddate=date.today()+timedelta(days=1))
    for transaction in transactionsQ:
        person = transaction.borrower_id
        email = User.query.filter_by(id=person).first().email
        book = transaction.book_id
        send_email(email,"remind",book)
