#initialises empty/non-existent database
import sqlite3
con=sqlite3.connect('mapped_out.db')
cur=con.cursor()

#posts table
cur.execute("CREATE TABLE IF NOT EXISTS posts (link text UNIQUE, description text, author text, longitude real, latitude real, location text)")
#will author be name or a user id number?
#location as string or as two ints -> latitude, longitude also dont they have N/S and E/W

try:
    cur.execute('''INSERT INTO posts VALUES ("https://www.youtube.com/watch?v=rEq1Z0bjdwc","Hello There","General Kenobi",53.4671,2.2342, "Manchester")''')
except sqlite3.Error as error:
    print(error)


#users table
cur.execute("CREATE TABLE IF NOT EXISTS users (name text, accessToken text UNIQUE)")

try:
    cur.execute('''INSERT INTO users VALUES ("General Kenobi","69420")''')
except sqlite3.Error as error:
    print(error)



con.commit()
print("POSTS:")
for row in cur.execute("SELECT * FROM posts"):
    print(row)

print("USERS:")
for row in cur.execute("SELECT * FROM users"):
    print(row)

con.close()
