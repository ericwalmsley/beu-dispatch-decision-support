//setup for basemap options
var usgsTopo_attrib = 'Map courtesy of <a href="https://usgs.gov/">USGS</a>',
	usgsImagery_attrib = 'Imagery courtesy of <a href="https://usgs.gov/">USGS</a>';
	
var usgsTopo_url = 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
	usgsImagery_url = 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}';

var usgsTopo = L.tileLayer(usgsTopo_url, {attribution: usgsTopo_attrib}),
	usgsImagery = L.tileLayer(usgsImagery_url, {attribution: usgsImagery_attrib});

//add map to div, set the view
var mymap = L.map('mapdiv', {
	layers: [usgsTopo]
	})
mymap.setView([36.2, -121], 9);

var baseLayers = {
'USGS Topo': usgsTopo,
'USGS Imagery': usgsImagery
};

let info = L.control({position: "bottomleft"});
info.onAdd = function() {
	let div = L.DomUtil.create("div", "info");
	div.innerHTML = '<h4>Fire Danger Rating Areas</h4><p id="currentFDRA"></p>';
	return div;
};
info.addTo(mymap);

//add the OSM background layer
//var backgroundLayer = L.tileLayer('http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
//	{attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'});
//mymap.addLayer(backgroundLayer);

//var maker = L.marker([36.4,-120.4],
//	{draggable: true,
//	title: 'Text that appears on hover',
//	opacity: 0.5}
//	).addTo(mymap);

//this is the lots of code way
//var hq_marker = L.marker([36.587363, -121.859116]);
//hq_marker.addTo(mymap);
//hq_marker.bindPopup("BEU Headquarters");

//this is the shorter way where you chain everything together
//var hq_marker = L.marker([36.587363, -121.859116], title='BEU Headquarters').addTo(mymap).bindPopup("BEU Headquarters");

//Pop-ups can include HTML and be complex, can literally be its own little webpage!
//hq_marker.bindPopup("<h3 class='text-center'>BEU Headquarters</h3><a href='https://www.fire.ca.gov/' target='blank'><img src='img/calfireblock_red.jpg' width='200px'></a>");

//jQuery function to zoom to beu
// can also use $("#zoom2beu").on("click", function(){
//$("#zoom2beu").click(function(){
//	mymap.setView([36.2, -121], 9);
//});

//$("#CT").click(function(){
//	mymap.fitBounds([
//	[36.68604, -120.94574],
//	[35.74874, -120.90866]
//	]);
//});

//Get lat long each time the mouse moves
mymap.on('mousemove', function(e){ //recall that toFixed sets # decimal places
	var str = "Latitude: " + e.latlng.lat.toFixed(5) + " Longitude: " + e.latlng.lng.toFixed(5);
	$("#map_coords").html(str);
});

//homework - create a function that adds a marker, with a popup containing the lat long, each time user clicks the map
//mymap.on('click', function(e){
	//var for lat
//	var lat = e.latlng.lat.toFixed(5);
	
	//var for longi
//	var longi = e.latlng.lng.toFixed(5);
	
	//create variable for mouse marker, and add to map                                    had to use a break here cause \n didn't work 
//	var mouse_marker = L.marker([lat, longi]).addTo(mymap).bindPopup("Latitude: " + lat + "<br>" + "Longitude: " + longi).openPopup();

	//deletes the marker when the popup is closed
//	mouse_marker.on('popupclose', function(){
//		mymap.removeLayer(mouse_marker);
//	});
//});

//declare a variable
var geojson;

//fx for assigning dispatch level
function dl_color(e){
	if (e == "Low") return "green";
	if (e == "Medium") return "yellow";
	if (e == "High") return "red";
}

//fx for grabbing dispatch level from FDRA
function get_dl(e){
	if (e == "Coastal Timber") return coti_dl;
	if (e == "Sierra de Salinas Shrub") return sds_dl;
	if (e == "Salinas Valley Grass") return svg_dl;
	if (e == "Gabilan Shrub") return gsh_dl;
	if (e == "Diablo Grass") return dgr_dl;
}

//fx to set colors
function baseColor(fdra) {
	return fdra == "Coastal Timber" ? dl_color(coti_dl) :
			fdra == "Sierra de Salinas Shrub" ? dl_color(sds_dl) :
			fdra == "Salinas Valley Grass" ? dl_color(svg_dl) :
			fdra == "Gabilan Shrub" ? dl_color(gsh_dl) :
			fdra == "Diablo Grass" ? dl_color(dgr_dl):
										"FFFFFF";
}

//fx for styling the polygons
function style(feature){
	return{
		fillColor: baseColor(feature.properties.fdra_name),
		weight: 2,
		opacity: 1, 
		color: 'white',
		dashArray:'3',
		fillOpacity: 0.75
	}; //end return
} //end fx

let info_p = document.getElementById("currentFDRA");

// function to highlihgt geojson features
function highlightFeature(e) {
	var layer = e.target;

	layer.setStyle({
		weight: 5,
		color: '#666',
		dashArray: '',
		fillOpacity: 0.55
	});

	if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
		layer.bringToFront();
	};
	
	info_p.innerHTML = "<br>" +
		layer.feature.properties.fdra_name + "<br>" + "<br>" +
		"Dispatch level: " + get_dl(layer.feature.properties.fdra_name);
}

//function to remove the highlight
function resetHighlight(e) {
	geojson.resetStyle(e.target);
	info_p.innerHTML="";
}

//function to fit to the zoomed feature
function zoomToFeature(e) {
	mymap.fitBounds(e.target.getBounds());
}

//tell
function onEachFeature(feature, layer) {
	layer.on({
		mouseover: highlightFeature,
		mouseout: resetHighlight,
		click: zoomToFeature
	})
//	if (feature.properties && feature.properties.fdra_name) {
//			layer.bindPopup(feature.properties.fdra_name);
};

// Add geojson atoms data that is hosted on github, mirrored by GitCDN.link
geojson = L.geoJson(fdras_beu, {
	style: style,
	onEachFeature: onEachFeature
}).addTo(mymap);

var overlays = {
	"FDRAs (SRA + FRA)": geojson,
	}

//legend
let legend = L.control({position: "topright"});
legend.onAdd = function() {
	let div = L.DomUtil.create("div", "legend"); 
	div.innerHTML = 
		'<b>Dispatch Level</b><br>' +
		'<div style="background-color: #ff0000"></div>High<br>' +
		'<div style="background-color: #FFFF00"></div>Medium<br>' +
		'<div style="background-color: #00FF00"></div>Low<br>';
	return div;
};
legend.addTo(mymap);

// layer on off panel
L.control.layers(baseLayers, overlays).addTo(mymap);