# this is the python file that actually hosts the website
# this should be the thing to create and display profiles
# anything to deal with updating the page (such as searching)
# should be done via javascript and api calls

from flask import Flask

app = Flask(__name__)
app.static_folder = "/static"

@app.route("/")
def landingPage():
    return open("static/landing/page.html", "r").read()

@app.route("/style.css")
def style():
    return open("static/landing/style.css", "r").read()