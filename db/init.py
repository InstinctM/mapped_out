#initialises empty/non-existent database
import sqlite3
con=sqlite3.connect('mapped_out.db')
cur=con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS posts (link text UNIQUE, description text, author text, longitude real, latitude real)")
#will author be name or a user id number?
#location as string or as two ints -> latitude, longitude also dont they have N/S and E/W

cur.execute('''INSERT INTO posts VALUES ("https://www.youtube.com/watch?v=rEq1Z0bjdwc","Hello There","General Kenobi",53.4671,2.2342)''')

con.commit()

for row in cur.execute("SELECT * FROM posts"):
    print(row)

con.close()