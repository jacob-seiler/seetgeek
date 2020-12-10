import datetime
import re


# ERROR CHECKERS
def validate_email(email):
    # Regex for validating email address
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if len(email) < 1:
        return "Email must not be empty."
    if not re.search(regex, email):
        return "Email format invalid."
    return False


def validate_name(name):
    if len(name) < 2 and len(name) > 20:
        return "Name must be between 2 and 20 characters."
    # Check if the name is all alphanumeric besides the spaces
    if not name.replace(" ", "").isalnum():
        return "Name must only contain alphanumeric characters or spaces."
    if name[0] == " " or name[-1] == " ":
        return "First and last characters can't be spaces."
    return False


def validate_password(password):
    # Bunch of if statements that check for at least one uppercase, lowercase and special character, length 6 or greater
    if len(password) < 7:
        return "Password must be at least 6 characters long."
    if not any(x.isupper() for x in password):
        return "Password must have at least one uppercase character."
    if not any(x.islower() for x in password):
        return "Password must have at least one lowercase character."
    if not any(not c.isalpha() for c in password):
        return "Password must have at least one special character."
    return False


def validate_ticket_name(name):
    """
    Validates that a given ticket name is valid
    :param name: The ticket name
    :return: True if name is valid
    """

    if not name.isalnum():
        return "Name must have alphanumeric characters only."
    if len(name) > 60:
        return "Name must be less than 60 characters."

    return False


def validate_ticket_quantity(quantity):
    try:
        quantity = int(quantity)
    except:
        return "Quantity must be an integer."
    if quantity < 1 or quantity > 100:
        return "Quantity must be between 1 and 100."
    return False


def validate_ticket_price(price):
    try:
        price = float(price)
    except:
        return "Price must be an integer"
    if price < 10 or price > 100:
        return "Price must be between 10 and 100 inclusive."
    return False


def validate_ticket_date(date):
    try:
        datetime.datetime.strptime(date, '%Y%m%d')
        return False
    except:
        return "Date must be in the format YYYYMMDD."


def validate_ticket(name, quantity, price, date):
    """
    Validates that all ticket data is correct
    :param name: The ticket name
    :param quantity: The ticket quantity
    :param price: The ticket price
    :param date: The ticket experation date
    :return: False if all data is valid, error message if not
    """

    error = validate_ticket_name(name)

    if error == False:
        error = validate_ticket_quantity(quantity)

    if error == False:
        error = validate_ticket_price(price)

    if error == False:
        error = validate_ticket_date(date)

    return error
