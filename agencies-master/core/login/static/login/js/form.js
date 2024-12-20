$(function () {

    const options = {
        enableHighAccuracy: true,
        timeout: 30000,
        maximumAge: 27000
    };

    const success = (pos) => {
        const crd = pos.coords;
        $('input[name="lat"]').val(crd.latitude);
        $('input[name="long"]').val(crd.longitude);
        $('input[name="accuracy"]').val(crd.accuracy);
    }

    const handleError = (error) => {
        // Display error based on the error code.
        const {code} = error;
        let errorMessage = '';

        switch (code) {
            case GeolocationPositionError.TIMEOUT:
                errorMessage = {'Tiempo agotado': ` Para continuar, Favor, recargue la página y asegúrese de tener localización activa - ${error.message}`};
                break;
            case GeolocationPositionError.PERMISSION_DENIED:
                // User denied the request.
                errorMessage = {'Permiso denegado': `Para continuar, favor dar permiso de Geolocalización y actualice - ${error.message}`};
                break;
            case GeolocationPositionError.POSITION_UNAVAILABLE:
                // Position not available.
                errorMessage = {'Posición no disponible': `Para continuar, Favor, recargue la página y asegúrese de tener localización activa - ${error.message}`};
                break;
        }
        message_error(errorMessage);
        // Intentar obtener la ubicación nuevamente si es un error recuperable
        retryGeolocation();
    }

    // navigator.geolocation.getCurrentPosition(success, handleError, options);

    const retryGeolocation = (attempts = 3) => {
        if (attempts > 0) {
            setTimeout(() => {
                navigator.geolocation.getCurrentPosition(success, handleError, options);
            }, 2000); // Esperar 2 segundos antes de reintentar
        } else {
            message_error({'Error': 'No se pudo obtener la ubicación después de varios intentos.'});
        }
    };

    retryGeolocation();

});