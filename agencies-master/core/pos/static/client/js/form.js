$(function () {
    select_user = $('select[name="user"]');

    $('input[type="checkbox"]').on('change', function (e) {
        let frequent = $('#id_frequent').prop('checked');
        let is_active = $('#id_is_active').prop('checked');

        if ((frequent && !is_active) && this.checked) {
            message_info({'Error de seleccion': 'Favor de desmarcar frecuente si tendrá días específicos de visita'})
        } else if (frequent && this.checked) {
            message_info({'Error de seleccion': 'Favor de desmarcar frecuente si tendrá días específicos de visita'})
        }
    });

});