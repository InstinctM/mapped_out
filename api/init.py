import db

confirm = input("Warning: This will clear the whole database. Do you want to continue? (y/n) ")
if ("n" in confirm.lower()):
    exit(0)

db.session.query(db.user).delete()
db.session.query(db.post).delete()
db.session.commit()

db.add_user(db.user(
    31415,
    "admin",
    "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", #password
    "",
    164800000,
    "GB",
    0,
))
db.add_user(db.user(
    43837,
    "beluga",
    "7b94103515005298262e40324ceb6c4922355267ee2b0ad1a6bb9d1dbbd6dc75", #skittle
    "",
    164800000,
    "US",
    0,
))
db.add_user(db.user(
    12345,
    "hello",
    "35a0c92fbcb2043dbff02e9c42078db2c2f8c3d356f4d7e44ab2f562e27417cf", #123qweASD
    "",
    164800000,
    "HK",
    0,
))

db.add_post(db.post(31415,"https://www.youtube.com/embed/kkLUneUgiI8","Kilburn Building Tour",0,53.46719182070933, -2.2341700730222045, "Kilburn Building, Oxford Road, Manchester, M13 9PL, United Kingdom"))
db.add_post(db.post(43837,"https://www.youtube.com/embed/pQN-pnXPaVg","HTML is a programming language",0,53.464920527372755, -2.233294173022296, "Alan Gilbert Learning Commons, Lime Grove, Manchester, M13 9PP, United Kingdom"))
db.add_post(db.post(12345,"https://www.youtube.com/embed/2TvRITW4M3M","Bruh central",0,53.48358035907067, -2.241522635215619, "Arndale Centre, Halle Place, Manchester, M4 2HU, United Kingdom"))


db.print_db()
