from flask import Flask, request, render_template

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
    loggedin = request.args.get('loggedin', default = "", type = str)
    if (loggedin == "true"):
        return render_template("user.html")
    return render_template("login.html")

@app.route("/signup", methods = ["GET"])
def signupPage():
    return render_template("signup.html")
