# Backend Test Case

# `login_user(email, password)`

| Partition | email   | password | result |
|-----------|---------|----------|--------|
| P1        | null    | null     | Fail   |
| P2        | null    | invalid  | Fail   |
| P3        | null    | valid    | Fail   |
| P4        | invalid | null     | Fail   |
| P5        | invalid | invalid  | Fail   |
| P6        | invalid | valid    | Fail   |
| P7        | valid   | null     | Fail   |
| P8        | valid   | invalid  | Fail   |
| P9        | valid   | valid    | Pass   |

Because this function has very few possible inputs, we are able to use exhaustive input testing to ensure that all the possible inputs are accounted for.

The test cases will cover the entire range of inputs for login_user.