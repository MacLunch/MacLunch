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
    var content = '<div id="pin-content">'+
      '<img id="pin-logo" src="/static/img/swmaestro.jpg" />' +
      '<div id="pin-body">' +
      '<h1 id="pin-info">소프트웨어 마에스트로 연수센터</h1>'+
      '<div id="bodyContent">'+
      '<p>서울 특별시 강남구 테헤란로 311(역삼동) 아남타워 빌딩 6층, 7층</p>'+
      '</div>'+
      '</div>'+
      '</div>';

    var mapOptions = {
      center: new google.maps.LatLng(37.503656, 127.045008),
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    var map = new google.maps.Map(mapCanvas, mapOptions);
    var marker = new google.maps.Marker({
    	position: {lat: 37.503656, lng: 127.045008},
    	map: map,
    	title: 'SWMaestro 연수센터',
    	label: 'SWMaestro 연수센터',
  	});
  	
  	var infowindow = new google.maps.InfoWindow({
    	content: content
	});

	marker.addListener('click', function() {
		infowindow.open(map, marker);
	});

	new google.maps.event.trigger( marker, 'click' );

}

function eqfeed_callback(results) {
  map.data.addGeoJson(results);
}


google.maps.event.addDomListener(window, 'load', init_map);