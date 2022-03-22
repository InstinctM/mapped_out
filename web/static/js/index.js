updateNavLoginBtn();
function updateNavLoginBtn() {
    const loginButton = document.getElementById("nav-login-btn");
    let username = localStorage.getItem("username");
    if (username != null) {
        loginButton.innerText = username;
    }
}

/// Clear localstorage to force user to login again
function logoutAll() {
    localStorage.removeItem("userid");
    localStorage.removeItem("username");
    localStorage.removeItem("token");
    localStorage.removeItem("tokenExpire");

    try {
        google.accounts.id.disableAutoSelect();
    } catch {
    }
}
