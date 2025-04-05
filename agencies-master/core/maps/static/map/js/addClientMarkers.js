/*carga finamica de markers*/
const sincronizacion = new Synchronization();

// Dibujamos los marcadores en el mapa
points.data.map((point) => {
    // Agregamos el marcador del cliente al mapa
    L.marker([point.lat, point.lng], {icon: redIcon}).addTo(map)
        .bindPopup(
            `<h2>${point.names}</h2> <p>${point.address}</p>`
        ).on('click', (e) => {
        let targetLat = `${e.latlng.lat}`;
        let targetLng = `${e.latlng.lng}`;

        var popUps = document.querySelectorAll('.leaflet-popup-content-wrapper');
        popUps.forEach(function (popUp) {
            popUp.addEventListener('click', async function (e) {

                // Buscamos en el array al cliente segun sus coordenadas
                const cliente = points.data.filter(point => point.lat === targetLat && point.lng === targetLng);

                // Verificamos si el cliente ya existe para insertarlo
                // antes de insertar los datos para que no elimine la data recolectada
                localforage.getItem(`${cliente[0].id}`)
                    .then(function (value) {
                        if (value === null) {
                            sincronizacion.guardarClientesLocalForage(cliente[0]);
                        }
                    })

                const url = `${pathname}`;
                let parameters = {
                    'action': 'client-detail',
                    'client': cliente[0]
                }

                const options = {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(parameters)
                };

                try {
                    const response = await fetch(pathname, options);
                    const result = await response.text();
                    //  Nos dirigimos al cliente solicitado
                    location.href = `${pathname}client-detail`;
                } catch (error) {
                    console.error(error)
                }

            });
        });
    })
});


// Centramos el mapa segun los marcadores
map.fitBounds([
    points.data.map(point => [point.lat, point.lng])
])