from flask import render_template, request, session, redirect
from qa327 import app
import qa327.backend as bn
import re

"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""


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

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, call the inner_function
                # with user as parameter
                return inner_function(user)
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner

@app.route('/sell')
def sell():
    return render_template('sell.html')

@app.route('/buy')
def buy():
    return render_template('buy.html')

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

@app.route('/', methods=['POST'])
def profile_post():
    print(request.form)
    if 'sell' in request.form:
        # TODO for future use
        # name = request.form.get('sell-form-name')
        # quantity = request.form.get('sell-form-quantity')
        # price = request.form.get('sell-form-price')
        # expiration_date = request.form.get('sell-form-expiration-date')

        return redirect('/sell', code=303)
    else:
        # TODO for future use
        # name = request.form.get('buy-form-name')
        # quantity = request.form.get('buy-form-quantity')

        return redirect('/buy', code=303)

# custom page for 404 error
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
