const loginButton = document.getElementById("nav-login-btn");
let username = localStorage.getItem("username");
if (username != null) {
    loginButton.innerText = username;
}

/// Clear localstorage to force user to login again
function logoutAll() {
    localStorage.setItem("userid", null);
    localStorage.setItem("username", null);
    localStorage.setItem("token", null);
    localStorage.setItem("tokenExpire", null);

    google.accounts.id.disableAutoSelect();
}
