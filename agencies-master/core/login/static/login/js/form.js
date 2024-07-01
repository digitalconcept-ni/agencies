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
        const {
            code
        } = error;
        switch (code) {
            case GeolocationPositionError.TIMEOUT:
                alert(`Tempo agotado, Para continuar, Favor, recargue la página y asegúrese de tener localización activa - ${error.message}`);
                break;
            case GeolocationPositionError.PERMISSION_DENIED:
                // User denied the request.
                alert(`Permiso denegado, Para continuar, favor dar permiso de Geolocalización y actualice - ${error.message}`);
                break;
            case GeolocationPositionError.POSITION_UNAVAILABLE:
                // Position not available.
                alert(`Posición no disponible, Para continuar, Favor, recargue la página y asegúrese de tener localización activa - ${error.message}`);
                break;
        }
    }

    navigator.geolocation.getCurrentPosition(success, handleError, options);

});