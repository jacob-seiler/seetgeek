# login_user()

### Test Cases
I chose to use condition coverage for my white-box test for login_user. There is one if statements with two conditions, which are as follows:

1) *not user*: This checks if user exists after `get_user()` is called, checks if user is in database.

2) *not check_password_hash(user.password, password)*: This checks if the user in the database has the same password as the one provided.

There are two conditions so our test cases will be: (T, T), (T, F), (F, T), (F, F)

### Implementation

- (T, T): This is actually impossible to implement. If the first condition is true, then there is no user to compare passwords against. 

- (T, F): We need to patch the get_user function so it returns None. Then we check if we get None, meaning the user wasn't able to log in.  

- (F, T): We need to patch the get_user function so it returns a test user. Then we check supply login_user with the test_user's info, but with a wrong password. The passwords wont match, and this will fail. This should return None, meaning login was unsuccessful. 

- (F, F): We patch get_user so the user exists in the database, and pass the user's password so the passwords match. This should return the User, meaning login was successful. 