const sincronizacion = new Synchronization();

(function () {

    var btnCheckin = document.getElementById("btn-checkin");
    var btnPedido = document.getElementById("btn-pedido");
    var btnCheckout = document.getElementById("btn-checkout");
    let date = new Date();
    let inputClientID = document.getElementById("input-id-client").value;

    // Inicializar valores en caso que existan
    sincronizacion.cargarInformacionDeLocalForage(inputClientID);


    // Evento del btn checkin
    btnCheckin.addEventListener("click", async function () {
        let hourCheckIn = `${date.getHours()}:${date.getMinutes()}`;
        let spanCheckOut = document.getElementById('checkin');
        this.classList.add('disabled')
        spanCheckOut.innerText = hourCheckIn;

        try {
            let coords = await getGeolocation();
            let latlng = [coords.latitude, coords.longitude];
            let campos = {
                checkin: `${hourCheckIn}`,
                checkinCoords: latlng
            }
            sincronizacion.agregarCamposLocalForage(`${inputClientID}`, campos)

        } catch (error) {
            message_error({'error': error})
        }
    })

    btnPedido.addEventListener("click", function () {
        // Gardamos en la session actual los datos del cliente para pasarlos en la siguiente vista
        localforage.getItem(`${inputClientID}`)
            .then(function (value) {
                if (value.hasOwnProperty('checkin')) {
                    sessionStorage.setItem(`cliente`, JSON.stringify(value));
                    // enviamos a la vista de facturacion
                    location.href = "/pos/sale/add/";
                } else {
                    message_error({'Info': 'Favor de dar primero Check-In'})
                }
            })

    })


    // Evento del btn chekout
    btnCheckout.addEventListener("click", function () {
        let hourCheckout = `${date.getHours()}:${date.getMinutes()}`;
        let spanCheckOut = document.getElementById('checkout');

        localforage.getItem(`${inputClientID}`).then(function (value) {
            if (value.hasOwnProperty('checkin')) {
                spanCheckOut.innerText = hourCheckout;
                // Optenemos los datos del cliente para agregarle
                // La hora del fin de la gestion
                sincronizacion.agregarCamposLocalForage(`${inputClientID}`, 'checkout', `${hourCheckout}`)
            } else {
                message_error({'Info': 'Favor de dar primero Check-In'})
            }
        })

    })
})();

