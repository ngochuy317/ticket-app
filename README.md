# Problem statement
1. A database table/model "Ticket" has 1 million rows:
 
   - Model: Ticket
     - Field: ID
     - Field: Token (UUID)

2. The table has a "token" column that holds a random unique UUID value for each row, determined by Django/Python logic at the time of creation. Due to a data leak, the candidate should write a django management command to iterate over every Ticket record to regenerate the unique UUID value.

3. The command should inform the user of progress as the script runs and estimates the amount of time remaining.

4. The script should also be sensitive to the potentially limited amount of server memory and avoid loading the full dataset into memory all at once, and show an understanding of Django ORM memory usage and query execution.

5. Finally, the script should ensure that if it is interrupted that it should save progress and restart near the point of interruption so that it does not need to process the entire table from the start.

# Solution
1. Loop to every record, generate the new UUID then update to Ticket. If IntegrityError occurs, generate UUID again until it unique. 
2. Limit the number of records in query to avoid out of memory.
3. Add a new column `is_regenerate` with default value is `False` to tracking if the record is re-generated

# Result
![command line](https://github.com/ngochuy317/ticket-app/blob/master/command_line_pic.png)