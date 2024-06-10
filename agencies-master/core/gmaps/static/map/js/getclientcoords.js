// file to get the client's coordinates
const mapDiv = document.getElementById('map');

let map;

async function initMap() {
    // Request libraries when needed, not in the script tag.
    const {Map} = await google.maps.importLibrary("maps");

    // Library for advanceMarker
    const {AdvancedMarkerElement, PinElement} = await google.maps.importLibrary("marker");
    // Short namespaces can be used.
    map = new Map(document.getElementById("map"), {
        center: {lat: userLat, lng: userLng},
        zoom: 18,
        mapId: 'e60eef08aec988f8',
    });

    // Create a marker to get customer's coordinate
    const marker = new AdvancedMarkerElement({
        position: {lat: userLat + 0.00019, lng: userLng},
        map: map,
        gmpDraggable: true,
        content: new PinElement({
            background: "#000080",
            borderColor: "#000080",
            glyphColor: 'white',
        }).element,
    });

    marker.addListener('dragend', function (event) {
        document.getElementById('latitud').value = event.latLng.lat();
        document.getElementById('longitud').value = event.latLng.lng();
        coordClient = true
    });


    // Marker User
    const markerUser = new AdvancedMarkerElement({
        map,
        position: {lat: userLat, lng: userLng},
        title: 'Mi posicion',
        // content: new PinElement({
        //     background: "#000080",
        //     borderColor: "#000080",
        //     glyphColor: 'white',
        // }).element,
    });

}

initMap();
// window.initMap = initMap;