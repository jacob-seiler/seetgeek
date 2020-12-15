from flask import flash, render_template, request, session, redirect
from qa327 import app
from qa327.backend import enough_balance, enough_tickets, ticket_exists
from qa327.utils import validate_email, validate_name, validate_password, validate_ticket, validate_ticket_date, validate_ticket_name, validate_ticket_price, validate_ticket_quantity
import qa327.backend as bn

"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""


@app.route('/register', methods=['GET'])
def register_get():
    # If user is logged in, redirect to /
    if 'logged_in' in session:
        return redirect("/")
    # If user is not logged in, serve the register page
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    # These helper functions return the error with a field if there is any, or False otherwise
    email_error = validate_email(email)
    name_error = validate_name(name)
    password_error = validate_password(password)

    if password != password2:
        error_message = "The passwords do not match"
    elif name_error:
        error_message = name_error
    elif email_error:
        error_message = email_error
    elif password_error:
        error_message = password_error
    else:
        user = bn.get_user(email)
        if user:
            error_message = "User exists"
        elif bn.register_user(email, name, password, password2):
            error_message = "Failed to store user info."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET'])
def login_get():
    # Check if the user is logged in, redirect to /
    if 'logged_in' in session:
        return redirect('/')
    else:
        return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    # Get info from form
    email = request.form.get('email')
    password = request.form.get('password')

    error_message = 'email/password combination incorrect'
    user = None

    # Check each condition and provide appropriate error message
    if len(password) == 0 and len(email) == 0:
        error_message = 'login failed'
    elif validate_email(email) is not False or validate_password(password) is not False:
        error_message = 'email/password format is incorrect.'
    else:
        user = bn.login_user(email, password)

    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between browser and the end server. Typically it is encrypted 
        and stored in the browser cookies. They will be past 
        along between every request the browser made to this services.

        Here we store the user object into the session, so we can tell
        if the client has already login in the following sessions.

        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message=error_message)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

    To wrap a function, we can put a decoration on that function.
    Example:

    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():
        user = None
        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)

            if user is None:
                del session['logged_in']

        if user:
            # if the user exists, call the inner_function
            # with user as parameter
            return inner_function(user)
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/sell', methods=['POST'])
def sell():
    # TODO for future use
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    expiration_date = request.form.get('date')

    # Check if each field has an error message or not
    name_error = validate_ticket_name(name)
    quantity_error = validate_ticket_quantity(quantity)
    price_error = validate_ticket_price(price)
    date_error = validate_ticket_date(expiration_date)

    # For each error, flash the message
    if name_error:
        flash(name_error)
    if quantity_error:
        flash(quantity_error)
    if price_error:
        flash(price_error)
    if date_error:
        flash(date_error)
    # If no errors, create ticket
    if not (name_error or quantity_error or price_error or date_error):
        create_error = bn.create_ticket(name, quantity, price, expiration_date)
        if create_error:
            flash(create_error)

    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    date = request.form.get('date')

    error_message = None

    if error_message == None:
        error_message = validate_ticket(name, quantity, price, date)

        if error_message == False:
            error_message = None

    if error_message == None:
        # The ticket of the given name must exist
        if not bn.ticket_exists(name):
            error_message = 'Ticket does not exist.'
        else:
            error_message = bn.update_ticket(name, quantity, price, date)

    if error_message is not None:
        flash(error_message)
    else:
        flash('Successfully updated ticket')

    # For any errors, redirect back to / and show an error message
    return redirect('/')


@app.route('/buy', methods=['POST'])
def buy():
    name = request.form.get('name')
    quantity = request.form.get('quantity')

    name_error = validate_ticket_name(name)
    quantity_error = validate_ticket_quantity(quantity) is not False
    exists_error = bn.ticket_exists(name) is False
    # user = bn.get_user(session['logged_in'])
    # balance_error = bn.enough_balance(user.balance, price, quantity)

    if name_error:
        flash("Invalid ticket.")
    elif exists_error:
        flash("Ticket does not exist.")
    elif quantity_error:
        flash("The request quantity is not available.")
    # if balance_error:
    #     flash("Insufficient balance")

    # For any errors, redirect back to / and show an error message
    return redirect('/')


@app.route('/')
@authenticate
def profile(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    tickets = bn.get_all_tickets()
    return render_template('index.html', user=user, tickets=tickets)

# custom page for 404 error


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
