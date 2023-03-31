import sqlite3

# connect to the database
conn = sqlite3.connect('theverge.db')

# create a cursor object
cursor = conn.cursor()

# execute a select statement
cursor.execute("SELECT * FROM articles")

# fetch all the rows
rows = cursor.fetchall()

# print the rows
for row in rows:
    print(row)

# close the connection
conn.close()