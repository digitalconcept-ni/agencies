// Configuracion del controlador de la base de datos
localforage.config({
    driver: [localforage.INDEXEDDB, localforage.WEBSQL, localforage.LOCALSTORAGE], // Force WebSQL; same as using setDriver()
    name: 'map',
    version: 1.0,
    size: 4980736, // Size of database, in bytes. WebSQL-only for now.
    storeName: 'clients', // Should be alphanumeric, with underscores.
    description: 'Lista de clientes a visitar'
});

class Synchronization {

    //Almacenar en el LS
    guardarClientesLocalForage(cliente) {
        localforage.setItem(`${cliente.id}`, cliente);
    }

    agregarCamposLocalForage(key, campos) {
        let _this = this;
        localforage.getItem(`${key}`)
            .then(function (value) {

                Object.entries(campos).forEach(([key, val]) => {
                    value[`${key}`] = val;
                    _this.guardarClientesLocalForage(value)
                })
            })
    }

    cargarInformacionDeLocalForage(cliente) {
        localforage.getItem(`${cliente}`)
            .then(function (value) {
                if (value !== null) {
                    // chechIn
                    let spanCheckIn = document.getElementById('checkin');
                    let spanCheckout = document.getElementById('checkout');
                    if (value.hasOwnProperty('checkin')) {
                        spanCheckIn.innerText = value['checkin'];
                        document.getElementById('btn-checkin').classList.add('disabled');
                    }
                    if (value.hasOwnProperty('checkout')) {
                        spanCheckout.innerText = value['checkout'];
                        document.getElementById('btn-checkout').classList.add('disabled');
                    }
                }
            })
    }

}