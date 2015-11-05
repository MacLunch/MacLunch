$(window).scroll(function(){
	var scrollHeight = $(window).scrollTop();
	var navBar = $("#full-navbar");

	if(scrollHeight >= 700) {
		if(navBar.hasClass("navbar-transparent") == true) {
			navBar.removeClass("navbar-transparent");
		}
	} else {
		if(navBar.hasClass("navbar-transparent") == false) {
			navBar.addClass("navbar-transparent");
		}
	}
});


function init_map() {
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


google.maps.event.addDomListener(window, 'load', init_map);