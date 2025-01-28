// carga finamica de markers


// Dibujamos los marcadores en el mapa
points.map((point) => {
    L.marker([point.lat, point.lng]).addTo(map)
        .bindPopup(
            `<p><b>Cliente:</b> ${point.names}</p> <p><b>  Telefono: </b> ${point.phone_number} </p>`
        )
});


// Centramos el mapa segun los marcadores
map.fitBounds([
    points.map(point => [point.lat, point.lng])
])