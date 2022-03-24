let lat;
let lon;

const map = L.map('map-select').setView([0, 0], 12);
map.setMinZoom(3).setMaxBounds([[90, -200], [-90, 200]]);

L.tileLayer(
    'https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=aEvyw1adgGE2cO8JBfZJ',
    {
        attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    }
).addTo(map);

let locSelMarker = L.marker([0, 0]).addTo(map);



getURLLocation();
function getURLLocation() {
    let param = new URLSearchParams(location.search);
    let lat = param.get("lat");
    let lon = param.get("lon");
    if (lat == null || lon == null) {
        geoip2.city((response) => {
            setLocation(response["location"]["latitude"], response["location"]["longitude"]);
        }, (error) => {
            console.log(error);
            setLocation(0, 0);
        });
    } else {
        setLocation(lat, lon);
    }
}

map.on('click', (e) => {
    let lat = e.latlng.lat;
    let lon = e.latlng.lng;

    setLocation(lat, lon);
});

function setLocation(selLat, selLon) {
    lat = selLat;
    lon = selLon;
    document.getElementById("location-txt").innerText =
        `Location: [${lat}, ${lon}]`;
    map.setView([lat, lon]);
    locSelMarker.setLatLng([lat, lon]);
}

function onPostVideo() {
    let title = document.getElementById("title").value;
    let ytVideoId = document.getElementById("link").value;
    let link = "https://www.youtube.com/embed/" + ytVideoId;

    if (title == "") {
        alert("Title is empty.");
        return;
    }
    if (ytVideoId.length < 5) {
        alert("Invalid video id");
        return;
    }

    let userid = localStorage.getItem("userid");
    let token = localStorage.getItem("token");
    let loc = "Do geocoding on backend";

    httpPost(API_URL + "/post", {
        "userid": userid,
        "token": token,
        "link": link,
        "description": title,
        "lat": lat,
        "lon": lon,
        "location": loc,
    }, (response) => {
        if (response["result"] == "success") {
            location.replace("/");
        } else if (response["result"] == "unauthorized") {
            alert("Error posting video: " + "Unauthorized.");
            logoutAll();
            location.replace("/login");
        } else {
            alert("Error posting video: " + JSON.stringify(response));
        }
    });
}
