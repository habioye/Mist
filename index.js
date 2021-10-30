let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.34657, lng: -74.65631 },
    zoom: 16,
  });
}
