// Configurations
const defaultLoc = [53.4674, -2.2339];  // [lat, lon]
const defaultRad = 100;  // radius is in miles
const defaultZoom = 10;  // 0-18

const heatMapRad = 25;
const heatMapWeight = 100;



let posts = {};

// use video link as key
let videoMarkers = {};
// new post marker
let newPostMarker = L.marker([0, 0]);

const map = L.map('map').setView(defaultLoc, defaultZoom);  // location, zoom
map.setMinZoom(3).setMaxBounds([[90, -200], [-90, 200]]);

L.tileLayer(
    'https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=aEvyw1adgGE2cO8JBfZJ',
    {
        attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    }
).addTo(map);

const heatLayer = L.heatLayer([], { radius: heatMapRad }).addTo(map);

map.on('click', onMapClick);
map.on('moveend', onMapMove);

getUserLocation();

function getUserLocation() {
    // Call some geolocation api to get user's location
    geoip2.city((response) => {
        let lat = response["location"]["latitude"];
        let lon = response["location"]["longitude"];
        //console.log(lat, lon);
        map.setView([lat, lon], defaultZoom);
        onMapMove(null);
    }, (error) => {
        console.log(error);
    });
}


function loadPosts(lat = defaultLoc[0], lon = defaultLoc[1], rad = defaultRad) {
    httpGet(API_URL + "/get-posts", {
        lat: lat,
        lon: lon,
        radius: rad,
    }, (response) => {
        //console.log(response);
        // response is an array of post objects

        if (response["result"] == "success") {
            response["posts"].forEach((post) => {
                let lat = post["latitude"];
                let lon = post["longitude"];
                let link = post["link"];

                posts[link] = post;

                if (videoMarkers[link] == null) {
                    let marker = L.marker([lat, lon]).addTo(map);
                    marker.bindPopup(getPopupElement(post), { maxWidth: "auto" });
                    videoMarkers[link] = marker;
                    heatLayer.addLatLng([lat, lon, heatMapWeight]);
                }
            });
        }

    });
}

function postUpdated(link) {
    videoMarkers[link].remove();
    delete videoMarkers[link];  // Force to get item from database again
    onMapMove(null);
}

function deleteVideo(userLink) {
    id = localStorage.getItem("userid");
    local_token = localStorage.getItem("token");
    if (!confirm("Are you sure to delete this video?")) return;
    httpPost(API_URL + "/delete", {
        userid: id,
        token: local_token,
        link: userLink
    }, (response) => {
        if (response) {
            postUpdated(userLink);
        } else {
            alert("Failed to delete video");
        }
    });
}

function editVideo(link) {
    let post = posts[link];
    let param = $.param(post);
    location.replace("/post-video?" + param);
}

function updateLikes(link, bool) {
    httpPost(API_URL + "/updateLikes", {
        link: link,
        like: bool,
    }, (response) => {
        if (response) {
            postUpdated(link);
        } else {
            console.log("Failed to like video");
        }
    });
}

function onMapMove(e) {
    const RAD_SCALE = 69;  // Convert degrees to miles (nice)
    let lat = map.getCenter()["lat"];
    let lon = map.getCenter()["lng"];
    let bounds = map.getBounds();
    let dx = bounds.getEast() - bounds.getWest();
    let dy = bounds.getNorth() - bounds.getSouth();
    let rad = Math.max(dx, dy) * RAD_SCALE;
    //console.log(`Map moved: [${lat}, ${lon}] => ${rad}`);

    loadPosts(lat, lon, rad);
}


// Select location for posting video
function onMapClick(e) {
    let lat = e.latlng.lat;
    let lon = e.latlng.lng;

    if (localStorage.getItem("userid") != null) {
        let newPostPopup = `
            <div class="row justify-content-between" style="width: 260px;">
                <div class="btn-group" role="group">
                    <button class="btn btn-primary" onclick="newPost(${lat}, ${lon})">Create New Post</button>
                    <button class="btn" style="color: gray;" onclick="closeNewPostPopup()"><i class="bi bi-x"></i></button>
                </div>
            </div>
        `;

        newPostMarker.setLatLng([lat, lon]);
        newPostMarker.addTo(map);
        newPostMarker.bindPopup(
            newPostPopup,
            {
                maxWidth: "auto",
                closeButton: false,
            }
        ).openPopup();
    }
}

function newPost(lat, lon) {
    closeNewPostPopup();
    location.replace(`/post-video?latitude=${lat}&longitude=${lon}`);
}

function closeNewPostPopup() {
    newPostMarker.closePopup();
    newPostMarker.remove();
}

function getPopupElement(post) {
    let link = post["link"];
    let username = localStorage.getItem("username");

    let deleteBtn = "";
    let editBtn = "";
    if (username == post["username"]) { // only display delete button if it is this user's video
        deleteBtn = `<button type="button" class="btn btn-danger" onclick="deleteVideo('${link}')"> <i class="bi bi-trash-fill"></i> </button>`;
        editBtn = `<button type="button" class="btn btn-light" onclick="editVideo('${link}')"> <i class="bi bi-pencil-fill"></i> </button>`;
    }

    let popupElement = `
    <div class="marker-popup" style="width: 480px; height: 420px;">
        <h4>${post["description"]}</h4>
        <div class="mx-auto" style="width: 460px; height: 260px;">
        <iframe width="460" height="260" src="${link}"
            allowfullscreen="allowfullscreen"
        ></iframe>
        </div>
        <br>
        <a class="mt-1" href="${link}">${link}</a>
        <p class="my-1">by <b>${post["username"]}</b></p>
        <p class="my-1">${post["likes"]} likes</p>

        <div class="row justify-content-between" style="width: 480px;">
            <div class="col-2 btn-group">
                <button type="button" class="btn btn-outline-primary" onclick="updateLikes('${link}',true)">
                    <i class="bi bi-hand-thumbs-up-fill"></i> </button>
                <button type="button" class="btn btn-outline-secondary" onclick="updateLikes('${link}',false)">
                    <i class="bi bi-hand-thumbs-down-fill"></i> </button>
            </div>
            <div class="col-2 btn-group">
                ${editBtn}
                ${deleteBtn}
            </div>
        </div>
    </div>
    `;

    return popupElement;
}


// resizing
onWindowResize();
window.addEventListener("resize", onWindowResize);
function onWindowResize() {
    let navbarHeight = document.getElementById("navbar").offsetHeight;
    document.getElementById("map").style.height = `calc(100% - ${navbarHeight}px)`;
}
