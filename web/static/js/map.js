// Get user locatoin?
let defaultLoc = [53.4674, -2.2339];  // [lat, lon]
let defaultRad = 1500;  // radius is in meters

const map = L.map('map').setView(defaultLoc, 12);  // location, zoom


const marker = L.marker(defaultLoc).addTo(map);
const cicrle = L.circle(defaultLoc, {
    radius: defaultRad, color: "red", fillColor: "green", fillOpacity: 0.2
}).addTo(map);

L.tileLayer(
    'https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=aEvyw1adgGE2cO8JBfZJ',
    {
        attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    }
).addTo(map);

map.on('click', onMapClick);


function onMapClick(e) {
    let lat = e.latlng.lat;
    let lon = e.latlng.lng;

    //console.log(`Marker location: [${lat}, ${lon}]`);

    marker.setLatLng([lat, lon]);
    cicrle.setLatLng([lat, lon]);

    marker.bindPopup(getPopupElement(lat, lon));
}


function getPopupElement(lat, lon) {
    // Get videos in this location
    let popupElement = `
    <h4>Video at [${lat.toFixed(4)}, ${lon.toFixed(4)}]</h4>
    <div class="border border-dark" style="width: 240px; height: 144px;">
    video preview
    </div>
    <p>https://youtube.url.here</p>
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
