from flask import Flask, request, render_template

# the following line loads the static folder into memory this means that when the server is running you cannot change the files that are displayed to the user
# without restarting the server, so if you make changes and want to see them restart the server
app = Flask(__name__, static_folder='static')

print("The server should now be online, if you are having problems connecting use http rather than https. We don't have a ssl certificate")

# Web Pages
@app.route("/", methods = ["GET"])
def landingPage():
    return render_template("map.html")

@app.route("/about", methods = ["GET"])
def aboutPage():
    return render_template("landpage.html")

@app.route("/login", methods = ["GET"])
def loginPage():
    loggedin = request.args.get('loggedin', default = "", type = str)
    if (loggedin == "true"):
        return render_template("user.html")
    return render_template("login.html")

@app.route("/user-edit", methods = ["GET"])
def userEditPage():
    return render_template("useredit.html")

@app.route("/signup", methods = ["GET"])
def signupPage():
    return render_template("signup.html")

@app.route("/post-video", methods = ["GET"])
def postVideo():
    return render_template("postvideo.html")

@app.route("/country-select", methods = ["GET"])
def countrySelect():
    return render_template("country-select.html")
