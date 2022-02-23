# this is the python file that actually hosts the website
# this should be the thing to create and display profiles
# anything to deal with updating the page (such as searching)
# should be done via javascript and api calls

from crypt import methods
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder='static')

@app.route("/", methods = ['GET'])
def landingPage():
    return render_template("mainpage.html")
