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

        let userid = response["userid"];
        let token = response["token"];
        // store userid and token to LocalStorage or cookie or whatever
    });
}

function onGoogleLogin() {
    console.log("Login with Google");
}
