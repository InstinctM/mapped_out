const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");


async function onLogin() {
    console.log("Login with username and password");
    let username = usernameInput.value;
    let password = passwordInput.value;

    let passwordBytes = new TextEncoder().encode(password);
    let hashedBytes = await window.crypto.subtle.digest("SHA-256", passwordBytes);
    let hashedArray = Array.from(new Uint8Array(hashedBytes));
    let hashed = hashedArray.map((bytes) => bytes.toString(16).padStart(2, "0")).join("");

    console.log(`username: ${username} | password: ${password} | hashed: ${hashed}`)

    $.get("http://127.0.0.1:8000/user-login", {
        "username": username,
        "password": hashed,
    }, (response) => {
        console.log(response);
    });
}

function onGoogleLogin() {
    console.log("Login with Google");
}
