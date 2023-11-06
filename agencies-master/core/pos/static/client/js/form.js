$(function () {
    select_user = $('select[name="user"]');

    $('input[name="birthdate"]').datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        maxDate: new Date()
    });

    // select_user.select2({
    //     theme: 'bootstrap4',
    //     language: "es",
    //     // allowClear: true,
    //     // placeholder: 'Usuario seleccionado'
    // });

    $('input[type="checkbox"]').on('change', function (e) {
        let frequent = $('#id_frequent').prop('checked');
        let is_active = $('#id_is_active').prop('checked');

        if ((frequent && !is_active) && this.checked) {
            message_error({'Error de seleccion': 'Favor de desmarcar frecuente si tendrá días específicos de visita'})
        } else if (frequent && this.checked) {
            message_error({'Error de seleccion': 'Favor de desmarcar frecuente si tendrá días específicos de visita'})
        }
    });


    $('#frmClient').on('submit', function (e) {
        e.preventDefault()
        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        // parameters.append('action', 'add');
        submit_with_ajax(pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            location.href = success_url;
        });
    })
});