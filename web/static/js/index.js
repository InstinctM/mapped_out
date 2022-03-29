const searchbox = document.getElementById("search");
const resultbox = document.getElementById("search-result");



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
    location.replace("/web/about");
}

function onNavSearch() {
    let kw = searchbox.value;
    resultbox.style.display = "none";
    httpGet(API_URL + "/search-post", {
        kw: kw,
        mode: "location",
    }, (response) => {
        let resultContent = "";
        if (response["result"] == "success") {
            if (response["posts"].length == 0) {
                resultContent += `<div class="search-post-entry"><p>No result</p></div>`;
            } else {
                response["posts"].forEach((post) => {
                    resultContent += `
                        <div class="search-post-entry" onclick="gotoPost(${post["latitude"]}, ${post["longitude"]})">
                            <h5>${post["description"]}</h5>
                            <p>@ ${post["location"]}</p>
                            <p>by ${post["username"]}</p>
                        </div>
                    `;
                });
            }
        } else {
            resultContent += `<div class="search-post-entry"><p>No result</p></div>`;
        }

        let searchboxWidth = searchbox.offsetWidth;
        resultbox.style.width = searchboxWidth + "px";
        resultbox.innerHTML = resultContent;
        console.log(resultContent);
        resultbox.style.display = "block";
    });
}



function gotoPost(lat, lon) {
    location.replace(`/web/?latitude=${lat}&longitude=${lon}`);
}


searchbox.oninput = () => {
    if (searchbox.value == "") {
        resultbox.style.display = "none";
    }
};

searchbox.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        onNavSearch();
    }
});
