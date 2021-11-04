let map;

function initMap() {

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.34657, lng: -74.65631 },
    zoom: 16,
  });
  const infoWindow = new google.maps.InfoWindow();

  const marker = new google.maps.Marker({
   position: { lat: 40.34657, lng: -74.65631 },
   map: map,
   // title: "title",
 });
 marker.addListener("click", () => {
      infoWindow.close();
      infoWindow.setContent(marker.getTitle());
      infoWindow.open(marker.getMap(), marker);
    });
}

// function addpoint(lat, long, text){
//   const marker = new google.maps.Marker({
//    position: { lat: lat, lng: long },
//    map: map,
//    title: text,
// }
