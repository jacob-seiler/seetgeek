from qa327.models import db, Ticket, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
"""
This file defines all backend logic that interacts with database and other services
"""


def get_user(email):
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
    user = User.query.filter_by(email=email).first()
    return user


def login_user(email, password):
    """
    Check user authentication by comparing the password
    :param email: the email of the user
    :param password: the password input
    :return: the user if login succeeds
    """
    # if this returns a user, then the name already exists in database
    user = get_user(email)
    if not user or not check_password_hash(user.password, password):
        return None
    return user


def register_user(email, name, password, password2):
    """
    Register the user to the database
    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :param password2: another password input to make sure the input is correct
    :return: an error message if there is any, or None if register succeeds
    """
    try:
        hashed_pw = generate_password_hash(password, method='sha256')
        # store the encrypted password rather than the plain password
        new_user = User(email=email,
                        name=name,
                        password=hashed_pw,
                        # balance=5000,
                        )

        db.session.add(new_user)
        db.session.commit()
        return None
    except:
        return "Unable to register user"


def get_all_tickets():
    """
    Retrieve all the tickets belonging to a specific user, identified by email
    :param email: The user's email
    :return: The list of tickets belonging to the user
    """

    # Gets todays date in format YYYYMMDD
    date_string = date.today().strftime('%Y-%m-%d').replace("-", "")

    # Query for all tickets where the expiration date is greater than or equal to current date
    ticket_list = Ticket.query.filter(Ticket.expiration_date >= date_string)

    return ticket_list
