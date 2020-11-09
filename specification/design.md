# Models

## User

id: int, primary key

email: string unique

name: string

password: string

balance: int

# Routes

## /register

### GET

When a GET request is made to register, we check to see if a login session is active for the user. 

If they are already logged in, redirect to `/` . 

Otherwise, render register.html

When they submit their webform, make a POST request to /register and pass the fields as parameters

### POST

Register can be broken up into parts:

- Form entry

    Get values from the form fields as parameters

- Form validation
    - Checking for non-empty fields
    - Validating password & username

        This can be done just by using a bunch of if statements

    - Validating email

        This can be done with regex

- Form handling
    - If form is handled with no errors, redirect user to `/login`
    - If there are any error, render register.html with the given error message

### Testing

- Testing that form works properly with the right conditions

    On a fresh database, register an account with the info:

    ```jsx
    name: "Tester Zero",
    email: "tester0@gmail.com",
    password1: "Password123"
    password2: "Password123" 
    ```

    This should result in a successful operation and redirect to login. There try logging in with the credentials:

    ```jsx
    email: "tester0@gmail.com",
    password: "Password123"
    ```

    If login is successful, the user should be redirected to `/` . Check that this is the case.

- Testing that correct error info is presented with the wrong conditions

    On a fresh database, run a loop that tries to register with info that is expected to throw an error. Example:

    ```jsx
    name: " Tester Zero ",
    email: "tester0@gmail.com",
    password1: "Password123"
    password2: "Password123" 
    ```

    If at any point the user is redirected to `/login` throw an error and fail the test.

## 404

### GET/POST

When a call is made to a non-existent endpoint, a status of 404 is returned, and 404.html is rendered

### Testing

Test that an invalid request returns a 404, and renders 404.html
