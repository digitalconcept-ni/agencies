const mapDiv = document.getElementById('map');

let map;
let markers = [];

const createMarker = (coord, name) => {
    let html = `<h4> ${name} </h4>`;
    const infowindow = new google.maps.InfoWindow({
        content: html,
        // ariaLabel: "Centro de los clientes",
    });

    const marker = new google.maps.Marker({
        position: coord,
        map: map,
    });

    // Funcion para ver la info de cada marcador en este caso de los clientes

    marker.addListener("click", () => {
        infowindow.open({
            anchor: marker,
            map,
        });
    });

    markers.push(marker)
}

const createLocationMarkers = () => {
    clients.forEach(cli => {
        let coord = new google.maps.LatLng(cli.lat, cli.lng);
        let name = cli.name;
        createMarker(coord, name);
    })
}

async function initMap() {
    // Request libraries when needed, not in the script tag.
    const { Map } = await google.maps.importLibrary("maps");
    // Short namespaces can be used.
    map = new Map(document.getElementById("map"), {
        center: { lat: 12.1294554, lng: -86.2248963 },
        zoom: 16,
    });

    createLocationMarkers();

    const marker = new google.maps.Marker({
        position: { lat: 12.1294554, lng: -86.2248963 },
        // position: { lat: userLat, lng: userLng },
        // position: google.maps.ControlPosition.TOP_CENTER,
        map: map,
        draggable: true,
    })

    marker.addListener('dragend', function (event) {
        console.log(this.getPosition().lat());
        console.log(this.getPosition().lng());
    })
}

initMap();
