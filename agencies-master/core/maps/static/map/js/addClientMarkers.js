// carga finamica de markers


// Dibujamos los marcadores en el mapa
points.map((point.data) => {
    L.marker([point.lat, point.lng]).addTo(map)
        .bindPopup(
            `<h4>${point.names}</h4> <p>${point.address}</p>`
        )
});


// Centramos el mapa segun los marcadores
map.fitBounds([
    points.map(point => [point.lat, point.lng])
])