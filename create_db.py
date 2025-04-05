import sqlite3

connection = sqlite3.connect('temperature.db')


with open('schema.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Enter a sample T and P value:

cur.execute("INSERT INTO temperature values(datetime('now', 'localtime'), 22.3)")
cur.execute("INSERT INTO pressure values(datetime('now', 'localtime'), 1013.5)")

connection.commit()
connection.close()