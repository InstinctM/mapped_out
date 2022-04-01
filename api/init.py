import db

"""
confirm = input("Warning: This will clear the whole database. Do you want to continue? (y/n) ")
if ("n" in confirm.lower()):
    exit(0)
"""

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
db.add_user(db.user(
   -8278426939280095492,
    "TheTraveller",
    "a0f3285b07c26c0dcd2191447f391170d06035e8d57e31a048ba87074f3a9a15",
    "92e75a672e05a198e67971b8aadd641fa372a11aca31a576bf2e56a108389419",
    1648823445,
    "AF",
    0
    ))



db.add_post(db.post(31415,"https://www.youtube.com/embed/kkLUneUgiI8","Kilburn Building Tour",0,53.46719182070933, -2.2341700730222045, "Kilburn Building, Oxford Road, Manchester, M13 9PL, United Kingdom"))
db.add_post(db.post(43837,"https://www.youtube.com/embed/pQN-pnXPaVg","HTML is a programming language",0,53.464920527372755, -2.233294173022296, "Alan Gilbert Learning Commons, Lime Grove, Manchester, M13 9PP, United Kingdom"))
db.add_post(db.post(12345,"https://www.youtube.com/embed/2TvRITW4M3M","Bruh central",0,53.48358035907067, -2.241522635215619, "Arndale Centre, Halle Place, Manchester, M4 2HU, United Kingdom"))
db.add_post(db.post(-8278426939280095492,"https://www.youtube.com/embed/huqJUghX26Y","Grand Canyon",0,37.4356124041315,-110.72296142578125,"Halls Crossing, San Juan County, Utah, United States of America"))
db.add_post(db.post(-8278426939280095492,"https://www.youtube.com/embed/aZ-31-p3saU","Effiel Tower Guide",0,48.85596226389368,2.2979450225830083,"Field of Mars, Rue de l'Université, 75007 Ile-de-France, France"))
db.add_post(db.post(-8278426939280095492,"https://www.youtube.com/embed/QA0WMIryzZs","Sydney Opera House",0,-33.8568428989929,151.21499955654147,"Sydney Opera House, 2 Macquarie Street, Sydney NSW 2000, Australia"))

db.print_db()
