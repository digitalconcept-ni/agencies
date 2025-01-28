/*Documento donde pondremos
las configuraciones del mapa*/


const map = L.map('map').setView([12.1304056,-86.2650888], 12);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
    attribution: '© OpenStreetMap'
}).addTo(map);