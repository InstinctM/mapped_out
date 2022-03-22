async function hashPassword(password) {
    let passwordBytes = new TextEncoder().encode(password);
    let hashedBytes = await window.crypto.subtle.digest("SHA-256", passwordBytes);
    let hashedArray = Array.from(new Uint8Array(hashedBytes));
    let hashed = hashedArray.map((bytes) => bytes.toString(16).padStart(2, "0")).join("");
    return hashed;
}

function validateUsername(username) {
    if (username.length < 3) return false;
    if (username.match(" ")) return false;
    return true;
}

function validatePassword(password) {
    if (password.length < 8) return false;
    if (!password.match("[a-z]") || !password.match("[A-Z]")) return false;
    if (!password.match("[0-9]")) return false;
    return true;
}

async function onSignup() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let password2 = document.getElementById("password2").value;
    let country = document.getElementById("country").value;

    if (!validateUsername(username)) {
        alert("Invalid username.");
        return;
    } else if (password != password2) {
        alert("Password mismatch.");
        return;
    } else if (!validatePassword(password)) {
        alert("Password must be at least 8-character long, contain upper and lower case letters and contain at least one numeric character.");
        return;
    }

    let hashed = await hashPassword(password);

    httpPost(API_URL + "/signup", {
        "username": username,
        "password": hashed,
        "country": country,
    }, (response) => {
        console.log("Create account: " + JSON.stringify(response));
        if (response != null) {
            alert("Successfully created a new account.");
            location.replace("/login");
        } else {
            alert("Failed to create an account: Username is taken, please try another username.");
        }
    });
}

async function onLogin() {
    console.log("Login with username and password");
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    let hashed = await hashPassword(password);

    httpPost(API_URL + "/user-login", {
        "username": username,
        "password": hashed,
    }, (response) => {
        console.log("Login: " + JSON.stringify(response));
        if (response == null) {
            alert("Login Failed.");
            return;
        }

        localStorage.setItem("userid", response["userid"]);
        localStorage.setItem("username", username);
        localStorage.setItem("token", response["token"]);
        localStorage.setItem("tokenExpire", response["tokenExpire"]);
        localStorage.setItem("loginMethod", "username");

        location.reload();
    });
}


function onGoogleLogin(response) {
    try {
        httpPost(API_URL + "/google-login", {
            token: response["credential"],
        }, (response) => {
            console.log("Google Login: " + JSON.stringify(response));
            if (response == null) {
                alert("Failed to login with Google.");
                return;
            }

            localStorage.setItem("userid", response["userid"]);
            localStorage.setItem("username", response["username"]);
            localStorage.setItem("token", response["token"]);
            localStorage.setItem("tokenExpire", response["tokenExpire"]);
            localStorage.setItem("loginMethod", "google");

            location.reload();
        });
    } catch {
        console.log("failed to decode jwt token");
        alert("Something went wrong...");
    }
}



function onLogout() {
    logoutAll();
    location.replace("/login");
}
