# SQL Injection Resiliance Report

## Scans Conducted

| Scan |            Route/URL           | Parameter | Number of Injection Trials | Number of Successful Trials |
|:----:|:------------------------------:|-----------|----------------------------|-----------------------------|
| 1    | http://127.0.0.1:8081/login    | email     | 14                         | 0                           |
| 1    | http://127.0.0.1:8081/login    | password  | 14                         | 0                           |
| 1    | http://127.0.0.1:8081/register | email     | 14                         | 0                           |
| 1    | http://127.0.0.1:8081/register | name      | 14                         | 0                           |
| 1    | http://127.0.0.1:8081/register | password  | 14                         | 0                           |
| 1    | http://127.0.0.1:8081/register | password2 | 14                         | 0                           |
| 2    | http://127.0.0.1:8081/sell     | name      | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/sell     | quantity  | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/sell     | price     | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/sell     | date      | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/buy      | name      | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/buy      | quantity  | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/update   | name      | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/update   | quantity  | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/update   | price     | 15                         | 0                           |
| 2    | http://127.0.0.1:8081/update   | date      | 15                         | 0                           |

## Takeaways

### Are all the user input fields in your application covered in all the test cases above? Any successful exploit?

All input fields were covered within the tests. The application was pretty straightforward, with the only forms being register, login, sell, buy and update forms. As you can see, all were covered in the table above.

There were no exploits that were successful. I would attribute this resiliance to SQLAlchemy, the ORM that we used for this project. It sanitizes the input by commenting out any special characters, so pretty much no SQL injections are possible, unless the user deliberately goes out of their way. We didn't use raw SQL, so we were covered.

### We did two rounds of scanning. Why the results are different? What is the purpose of adding in the session id?

Round one covered all the pages that are accessable by a user that is logged in, as you can see in the table above. Round two covered all pages that are restricted for authenticated users only. 

The session id token is used by flask to keep track of user sessions, meaning keep track of a user as they are logged in, so they don't have to log in at every new page. By providing to the scan, we were able to let the scan access restricted pages. 

### Summarize the injection payload used based on the logs, and breifly discuss the purpose.

Here is an example log of one of the variables: 

```
[02:04:42] [WARNING] POST parameter 'price' does not appear to be dynamic
[02:04:42] [WARNING] heuristic (basic) test shows that POST parameter 'price' might not be injectable
[02:04:42] [INFO] testing for SQL injection on POST parameter 'price'
[02:04:42] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[02:04:42] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[02:04:42] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[02:04:42] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[02:04:42] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[02:04:42] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[02:04:42] [INFO] testing 'Generic inline queries'
[02:04:42] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[02:04:42] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[02:04:43] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[02:04:43] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[02:04:43] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[02:04:43] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[02:04:43] [INFO] testing 'Oracle AND time-based blind'
[02:04:43] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[02:04:44] [WARNING] POST parameter 'price' does not seem to be injectable
```

First, the scan starts off by doing a heuristic scan, guessing if the parameter is injectible. Then, each line represents a known exploit for different SQL servers. For example, line 7 tests an exploit specific to PostgreSQL, seeing if it is able to access any data. 