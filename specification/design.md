# Models

## User

id: int, primary key

email: string unique

name: string

password: string

balance: int

# Routes

## /login

### GET

When a GET request is made to register, we check to see if a login session is active for the user.

If they are already logged in, redirect to `/` .

Otherwise, render login.html

When they submit their webform, make a POST request to /login and pass the fields as parameters

### POST

Login can be broken up into these parts:

-   Form entry

    Get values from the form fields as parameters

-   Form validation

    -   Checking for non-empty fields
    -   Validating password & username

        This can be done just by using a bunch of if statements

    -   Validating email

        This can be done with regex

-   Form handling
    -   If form is handled with no errors, redirect user to `/`
    -   If there are any error, render login.html with the given error message

### Testing

-   Testing that form works properly with the right conditions

    On a fresh database, register an account with the info:

    ```jsx
    name: "Tester Zero",
    email: "tester0@gmail.com",
    password1: "Password123",
    password2: "Password123"
    ```

    This should result in a successful operation and redirect to login. There try logging in with the credentials:

    ```jsx
    email: "tester0@gmail.com",
    password: "Password123"
    ```

    If login is successful, the user should be redirected to `/` . Check that this is the case.

-   Testing that correct error info is presented with the wrong conditions

    On a fresh database, run a loop that tries to login with info that is expected to throw an error. Example:

    ```jsx
    email: "hello",
    password: "password123"
    ```

    If at any point the user is redirected to `/` throw an error and fail the test.

## /register

### GET

When a GET request is made to register, we check to see if a login session is active for the user.

If they are already logged in, redirect to `/` .

Otherwise, render register.html

When they submit their webform, make a POST request to /register and pass the fields as parameters

### POST

Register can be broken up into these parts:

-   Form entry

    Get values from the form fields as parameters

-   Form validation

    -   Checking for non-empty fields
    -   Validating password & username

        This can be done just by using a bunch of if statements

    -   Validating email

        This can be done with regex

-   Form handling
    -   If form is handled with no errors, redirect user to `/login`
    -   If there are any error, render register.html with the given error message

### Testing

-   Testing that form works properly with the right conditions

    On a fresh database, register an account with the info:

    ```jsx
    name: "Tester Zero",
    email: "tester0@gmail.com",
    password1: "Password123",
    password2: "Password123"
    ```

    This should result in a successful operation and redirect to login. There try logging in with the credentials:

    ```jsx
    email: "tester0@gmail.com",
    password: "Password123"
    ```

    If login is successful, the user should be redirected to `/` . Check that this is the case.

-   Testing that correct error info is presented with the wrong conditions

    On a fresh database, run a loop that tries to register with info that is expected to throw an error. Example:

    ```jsx
    name: " Tester Zero ",
    email: "tester0@gmail.com",
    password1: "Password123",
    password2: "Password123"
    ```

    If at any point the user is redirected to `/login` throw an error and fail the test.

## /

### GET

When a GET request is made to `/``, we check to see if a login session is active for the user.

If they are not logged in, redirect to `/login` .

Otherwise, render `login.html`

### Testing

Test that `/` loads after login

## /sell

### POST

Validates ticket information provided from form. If all fields are valid, a new ticket is created

### Testing

-   Testing that ticket creation works

    On a fresh database, create a ticket with the following data:

    ```jsx
    name: "Test",
    quantity: 25,
    price: 50.0,
    expiration_date: 2050-11-28
    ```

    If successful, the user should be redirected to `/` and the new ticket data should be displayed. Check that this is the case.

-   Testing that correct error info is presented with the wrong conditions

    On a fresh database, after a ticket is created, run a loop that tries to update ticket information with data expected to give an error. Example:

    ```jsx
    name: "Test",
    quantity: "hello",
    price: 75.0,
    expiration_date: 2077-12-10
    ```

    If at any point an error message is not displayed, throw an error and fail the test.



## /update

### POST

Validates ticket information provided from form. If valid and if ticket with the same name exists, updates ticket.

### Testing

-   Testing that ticket validation works and updates correctly

    On a fresh database, create a ticket with the following data:

    ```jsx
    name: "Test",
    quantity: 25,
    price: 50.0,
    expiration_date: 2050-11-28
    ```

    Now try to update the ticket with the following data:

    ```jsx
    name: "Test",
    quantity: 30,
    price: 75.0,
    expiration_date: 2077-12-10
    ```

    If update is successful, the user should be redirected to `/` and the updated ticket data should be displayed. Check that this is the case.

-   Testing that correct error info is presented with the wrong conditions

    On a fresh database, after a ticket is created, run a loop that tries to update ticket information with data expected to give an error. Example:

    ```jsx
    name: "Test",
    quantity: "hello",
    price: 75.0,
    expiration_date: 2077-12-10
    ```

    If at any point an error message is not displayed, throw an error and fail the test.

## /buy

## /update

### POST

Validates ticket information provided from form. If valid, ticket with the same name exists, user has a sufficient balance and enough tickets exist, buys ticket.

### Testing

-   Testing that ticket validation works and purchases correctly

    On a fresh database, create a ticket with the following data:

    ```jsx
    name: "Test",
    quantity: 25,
    price: 50.0,
    expiration_date: 2050-11-28
    ```

    Now try to buy the ticket with the following data:

    ```jsx
    name: "Test",
    quantity: 25,
    price: 50,
    expiration_date: 2050-11-28
    ```

    If purchase is successful, the user should be redirected to `/` and the ticket should be transferred over to them. Check that this is the case.

-   Testing that correct error info is presented with the wrong conditions

    On a fresh database, after a ticket is created, run a loop that tries to purchase tickets with data expected to give an error. Example:

    ```jsx
    name: "Test",
    quantity: "hello",
    price: 75.0,
    expiration_date: 2077-12-10
    ```

    If at any point an error message is not displayed, throw an error and fail the test.

## /logout

### GET/POST

When a call is made to logout, invalidate the current session and redirect to the login page

### Testing

Test that when /logout is visited, the user is redirected to `/login` and the login screen is displayed

## 404

### GET/POST

When a call is made to a non-existent endpoint, a status of 404 is returned, and 404.html is rendered

### Testing

Test that an invalid request returns a 404, and renders 404.html
