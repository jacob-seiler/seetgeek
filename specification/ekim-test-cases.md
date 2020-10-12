# Untitled

# R4: '/sell'

### The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character

- Check if string is alphanumeric using isalnum() in python
- Check that the first character isn't a space and the last character isn't a space

### The name of the ticket is no longer than 60 characters

- Check if len(ticket) > 60.

### The quantity of the tickets has to be more than 0, and less than or equal to 100

- Check quantity > 0 && quantity < 100.

### Price has to be of range [10, 100]

- Check that price ≥ 10 and price ≤ 100

### Date must be given in the format YYYYMMDD (e.g. 20200901)

- Check that the date is all numerical using isnum() in python
- Check that the length of the date is exactly 8
- Check that the month substring (date[5:6]) is greater than 0 and less than 13 and check that the date substring (date[7:]) is greater than 0 and less than 31. This can be done by parsing the date into a python datetime object, if it isn't valid an error will be thrown.

### The added new ticket information will be posted on the user profile page

- Check using selenium that the new ticket appears on the user's page

### For any errors, redirect back to / and show an error message

- If any of the conditions above fail, redirect to '/' with an error state

# R5: '/update'

### The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character

- Check if string is alphanumeric using isalnum() in python
- Check that the first character isn't a space and the last character isn't a space

### The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character

- Check if string is alphanumeric using isalnum() in python
- Check that the first character isn't a space and the last character isn't a space

### The name of the ticket is no longer than 60 characters

- Check if len(ticket) > 60.

### The quantity of the tickets has to be more than 0, and less than or equal to 100

- Check quantity > 0 && quantity < 100.

### Price has to be of range [10, 100]

- Check that price ≥ 10 and price ≤ 100

### The ticket of the given name must exist

- Check that an SQL query with name = request_name doesn't return NULL.

### Date must be given in the format YYYYMMDD (e.g. 20200901)

- Check that the date is all numerical using isnum() in python
- Check that the length of the date is exactly 8
- Check that the month substring (date[5:6]) is greater than 0 and less than 13 and check that the date substring (date[7:]) is greater than 0 and less than 31. This can be done by parsing the date into a python datetime object, if it isn't valid an error will be thrown.

### For any errors, redirect back to / and show an error message

- If any of the conditions above fail, redirect to '/' with an error state

# R6: '/buy'

### The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character

- Check if string is alphanumeric using isalnum() in python
- Check that the first character isn't a space and the last character isn't a space

### The name of the ticket is no longer than 60 characters

- Check if len(ticket) > 60.

### The quantity of the tickets has to be more than 0, and less than or equal to 100

- Check quantity > 0 && quantity < 100.

### The ticket name exists in the database and the quantity is more than the quantity requested to buy

- Check that an sql query where name = name_requested doesn't return NULL
- Check that the result of the query has quantity > quantity_requested

### The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)

- Query the current user in the database, and get his current balance. Calculate the final cost by (price * quantity * 1.35 * 1.05). Check that balance > final cost.

### For any errors, redirect back to / and show an error message

- If any of the conditions above fail, redirect to '/' with an error state
