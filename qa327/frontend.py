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


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None


    if password != password2:
        error_message = "The passwords do not match"

    elif len(email) < 1:
        error_message = "Email format error"

    elif len(password) < 1:
        error_message = "Password not strong enough"
    else:
        user = bn.get_user(email)
        if user:
            error_message = "User exists"
        elif not bn.register_user(email, name, password, password2):
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
    elif not email_formatted(email) or not pasword_is_complex(password):
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

"""
Checks if email is formatted correctly
Takes string email
Returns True if formatted properly
"""
def email_formatted(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # Apply regex to email
    return re.search(regex, email)

"""
Checks if password has required complexity
Takes string password
Returns True if complexity is met
"""
def pasword_is_complex(password):
    # Minimum length 6
    if len(password) < 6:
        return False

    # At least one upper case, lower case, and special character
    has_upper = False
    has_lower = False
    has_special = False

    # Check every character for instance
    for c in password:
        if c.isupper():
            has_upper = True
        else:
            has_lower = True
        
        if not c.isalnum():
            has_special = True
    
    return has_upper and has_lower and has_special

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
