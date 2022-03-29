checkLoginStatus();
updateNavBtns();

function updateNavBtns() {
    const loginButton = document.getElementById("nav-login-btn");
    const newPostButton = document.getElementById("new-post-btn");
    let username = localStorage.getItem("username");
    if (username != null) {
        loginButton.innerText = username;
        newPostButton.style.display = "block";
    }

}


let firstTime = localStorage.getItem("first-time");
if (firstTime == null) {
    localStorage.setItem("first-time", false);
    location.replace("/about");
}

function onNavSearch() {
    let kw = document.getElementById("search").value;
    httpGet(API_URL + "/search-post", {
        kw: kw,
    }, (response) => {
        console.log(response);
    });
}
