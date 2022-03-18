import db

db.add_user(69420,"General_Kenobi_XIV","verysnek",1668203967,"United Kingdom",999)
db.add_user(123456,"John Smith","password",1669203964,"United States",1)
db.add_user(98765,"Da Ali G", "password2",1669203964,"united Kingdom",13)

db.add_post(69420,"https://www.youtube.com/watch?v=rEq1Z0bjdwc","Hello There.",11,53.46719182070933, -2.2341700730222045, "Kilburn Building")
db.add_post(123456,"https://youtu.be/efgIm9YPZvE","Ali G inda house",22,53.464920527372755, -2.233294173022296, "Alan Gilbert Learning Commons")
db.add_post(98765,"https://www.youtube.com/watch?v=2TvRITW4M3M","Bruh central",33,53.48358035907067, -2.241522635215619, "Manchester Arndale")


print("-------- Users --------")
for user in db.session.query(db.user):
    repr(user)
print()
print("----------------")


print("-------- Posts --------")
for post in db.session.query(db.post):
    repr(post)
print()
print("----------------")