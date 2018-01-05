var default_poisition = {lat: -34.397, lng: 150.644}
var infowindow;
var map;
var pos;

function initMap(){
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 17,
		center: default_poisition
	});

	get_current();
}

const get_current = () =>{
	if (navigator.geolocation){
		navigator.geolocation.getCurrentPosition((position) =>{
			pos = {
				lat: position.coords.latitude,
				lng: position.coords.longitude
			};
			let marker = new google.maps.Marker({ position: pos, map: map});
			let content = "Location is founded";
			map.setCenter(pos);
			marker.addListener("click", () =>{
				infowindow.open(map, marker);
				infowindow.setContent(content);
			});
		}, () =>{
			alert("Location is not founded!");
		});	
	}
}

$("#map_modal").on("shown.bs.modal", (e) => {
	google.maps.event.trigger(map, "resize")
	return map.setCenter(pos)
})


