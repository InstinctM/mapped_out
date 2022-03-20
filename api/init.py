import db

"""
db.add_user(db.user(69420,"General_Kenobi_XIV","verysnek","token0332432",1668203967,"United Kingdom",999))
db.add_user(db.user(123456,"John Smith","password","token2378714",1669203964,"United States",1))
db.add_user(db.user(98765,"Da Ali G", "password2","token3423478",1669203964,"United Kingdom",13))
"""
db.add_user(db.user(
    31415,
    "admin",
    "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    "",
    164800000,
    "United Kingdom",
    69,
))
db.add_user(db.user(
    43837,
    "beluga",
    "7b94103515005298262e40324ceb6c4922355267ee2b0ad1a6bb9d1dbbd6dc75",
    "",
    164790000,
    "United States",
    0,
))

db.add_post(db.post(69420,"https://www.youtube.com/watch?v=rEq1Z0bjdwc","Hello There.",11,53.46719182070933, -2.2341700730222045, "Kilburn Building"))
db.add_post(db.post(123456,"https://youtu.be/efgIm9YPZvE","Ali G inda house",22,53.464920527372755, -2.233294173022296, "Alan Gilbert Learning Commons"))
db.add_post(db.post(98765,"https://www.youtube.com/watch?v=2TvRITW4M3M","Bruh central",33,53.48358035907067, -2.241522635215619, "Manchester Arndale"))


db.print_db()
