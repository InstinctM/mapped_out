import db

outfile = open("init.py", "w")

outfile.writelines([
    "import db\n",
    "db.session.query(db.user).delete()\n",
    "db.session.query(db.post).delete()\n",
    "db.session.commit()\n",
])

users = db.session.query(db.user)
posts = db.session.query(db.post)

for user in users:
    outfile.write(
        f"db.add_user(db.user({user.userid}, \"{user.username}\", \"{user.password}\", \"{user.token}\", {user.tokenExpire}, \"{user.country}\", {user.points}))\n"
    )


for post in posts:
    outfile.write(
            f"db.add_post(db.post({post.author}, \"{post.link}\", \"{post.description}\", {post.likes}, {post.latitude}, {post.longitude}, \"{post.location}\"))\n"
    )

outfile.write("db.print_db()\n")
outfile.close()
