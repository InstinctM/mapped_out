// use video link as key
let videoMarkers = {};


// Get user locatoin?
let defaultLoc = [53.4674, -2.2339];  // [lat, lon]
let defaultRad = 15000;  // radius is in meters

const map = L.map('map').setView(defaultLoc, 12);  // location, zoom


L.tileLayer(
    'https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=aEvyw1adgGE2cO8JBfZJ',
    {
        attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    }
).addTo(map);

map.on('click', onMapClick);
map.on('moveend', onMapMove);


loadPosts();

function addMarkers(newMarkers) {
    videoMarkers.forEach((marker) => {
        if (!marker in newMarkers) {
            marker.remove()
        }
    });
    videoMarkers = newMarkers;
}

function loadPosts(lat = defaultLoc[0], lon = defaultLoc[1], rad = defaultRad) {
    httpGet(API_URL + "/get-posts", {
        lat: lat,
        lon: lon,
        radius: rad,
    }, (response) => {
        //console.log(response);
        // response is an array of post objects

        response.forEach((post) => {
            let lat = post["latitude"];
            let lon = post["longitude"];
            let link = post["link"];

            if (videoMarkers[link] == null) {
                let marker = L.marker([lat, lon]).addTo(map);
                marker.bindPopup(getPopupElement(post), { maxWidth: "auto" });
                videoMarkers[link] = marker;
            }
        });

    });
}

function deleteVideo(userLink){
    
    id = localStorage.getItem("userid")
    local_token = localStorage.getItem("token")
    httpPost(API_URL + "/delete",{
        userid  : id,
        token : local_token,
        link: userLink
    }, (response) =>{
        console.log(response)
    }
    )
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


function onMapClick(e) {
    let lat = e.latlng.lat;
    let lon = e.latlng.lng;
}

function getPopupElement(post) {
    let link = post["link"];

    let popupElement = `
    <div class="marker-popup" style="width: 480px; height: 400px;">
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
        <button type = "button" onclick="deleteVideo('${link}')"> Delete </button>
        <button type = "button"> Like </button>

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
