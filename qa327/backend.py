from qa327.models import db, Ticket, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
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


def get_ticket(name):
    """
    Gets a ticket by given name
    :param name: The ticket name to search for
    :return: True if a ticket with the given name exists
    """

    return Ticket.query.filter_by(name=name).first()


def update_ticket(name, quantity, price, date):
    """
    Updates ticket quantity, price, and expiration date
    :param name: The ticket name to update
    :param quantity: The new quantity
    :param price: The new price
    :param date: The new expiration date
    """

    ticket = get_ticket(name)

    if ticket is not None:
        try:
            ticket.quantity = int(quantity)
            ticket.price = float(price)
            ticket.expiration_date = datetime.strptime(date, '%Y%m%d')
            db.session.commit()
            return None
        except:
            return 'Could not update ticket'


def validate_ticket(name, quantity, price, date):
    """
    Validates that all ticket data is correct
    :param name: The ticket name
    :param quantity: The ticket quantity
    :param price: The ticket price
    :param date: The ticket experation date
    :return: True if all data is valid
    """

    # Validate types
    try:
        quantity = int(quantity)
        price = float(price)
    except ValueError:
        return False

    # The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
    for i in range(len(name)):
        char = name[i]
        if char == ' ' and (i == 0 or i == len(name) - 1):
            return False
        elif not char.isalnum():
            return False

    # The name of the ticket is no longer than 60 characters
    if (len(name) > 60):
        return False

    # The quantity of the tickets has to be more than 0, and less than or equal to 100.
    if (quantity <= 0 or quantity > 100):
        return False

    # Price has to be of range [10, 100]
    if (price < 10 or price > 100):
        return False

    # Date must be given in the format YYYYMMDD (e.g. 20200901)
    try:
        datetime.strptime(date, '%Y%m%d')
    except ValueError:
        return False

    return True
