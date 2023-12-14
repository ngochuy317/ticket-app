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
1. Loop to every record, generate the new UUID then update to Ticket. If IntegrityError occurs, generate UUID again until it is unique. 
2. In the first time, I was use the query

```python
Ticket.objects.all()
```

To avoid out of memory I limit the number of records in query with
```python
Ticket.objects.order_by("-id")[: self.CHUNKSIZE]
```
3. About the checkpoint if there is an interrupt issue, I add a new column `is_regenerate` with default value is `False` to track if the record is re-generated.
So the filter condition was added
```python
.filter(is_regenerate=False)
```
Then when the command runs again, it will not re-generate for all the records. The time will be more slower with this one but we can trace back the lasted record update successfully


# Result
![command line](https://github.com/ngochuy317/ticket-app/blob/master/command_line_pic.png)

# Running the project

1. Requirement:
   - Python 3.11
2. Install the project dependencies with

```
pip install -r requirements.txt
```
3. Init data
```
python manage.py migrate ticket
```
4. Run command re-generate token
```
python manage.py regenerate_uuid
```