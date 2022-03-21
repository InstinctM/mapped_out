from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

# Web Pages
@app.route("/", methods = ["GET"])
def landingPage():
    return render_template("map.html")

@app.route("/about", methods = ["GET"])
def aboutPage():
    return render_template("about.html")

@app.route("/login", methods = ["GET"])
def loginPage():
    return render_template("login.html")

@app.route("/signup", methods = ["GET"])
def signupPage():
    return render_template("signup.html")
