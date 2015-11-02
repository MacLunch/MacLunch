
function initialize() {
    var mapCanvas = document.getElementById('map');
    var mapOptions = {
      center: new google.maps.LatLng(37.503656, 127.045008),
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(mapCanvas, mapOptions);
}
function eqfeed_callback(results) {
  map.data.addGeoJson(results);
}


google.maps.event.addDomListener(window, 'load', initialize);