import datetime
from .Models import Subscribers
from . import db

def send_newsletter_if_needed():
    # Check if the current day is Wednesday (Wednesday is represented by 2 in Python's datetime module)
    if datetime.datetime.now().weekday() == 2:
        # Check if the newsletter has not been sent yet
        if not newsletter_already_sent():
            # Send the newsletter to all subscribers
            send_newsletter_to_subscribers()
            # Mark that the newsletter has been sent
            mark_newsletter_as_sent()

def newsletter_already_sent():
    # Check if the newsletter has been sent
    # You can implement this function based on your database structure
    # For example, you can check if there are any entries in the Subscribers table with the status "sent"
    # Return True if the newsletter has already been sent, False otherwise
    return Subscribers.query.filter_by(status='sent').first() is not None

def send_newsletter_to_subscribers():
    # Code to send the newsletter to all subscribers
    # This part is similar to the code you provided for sending the newsletter
    pass

def mark_newsletter_as_sent():
    # Update the database to mark the newsletter as sent
    # For example, you can update the status column of the Subscribers table to "sent" for all subscribers
    # You can use an ORM (Object-Relational Mapping) library like SQLAlchemy to perform database operations
    subscribers = Subscribers.query.all()
    for subscriber in subscribers:
        subscriber.status = 'sent'
    db.session.commit()

# Call the function to check if the newsletter needs to be sent
send_newsletter_if_needed()
