var assets = {
    config: [
        {
            targets: [0],
            visible: false,
        },
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a href="' + pathname + 'update/' + row[0] + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                buttons += '<a rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                return buttons;
            }
        },],
    list: function (action) {

        let data = {
            'data': action,
            'inserInto': 'rowList',
            'th': ['Nro', 'Cliente', 'Activo', 'Cantidad', 'Fecha entrega', 'Marca', 'Código', 'Serie', 'Opciones'],
            'table': 'tableList',
            'config': assets.config,
            'modal': false,
        }
        drawTables(data);
    }
};

$(function () {

    select_client = $('select[name="client"]');

    select_client.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_client'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese Nombre o Número de cédula',
        minimumInputLength: 1,
    });

    // client.list();

    $('#btnSearch').on('click', function () {

        let clientId = $('#search_client').val();
        console.log(clientId)

        if (clientId === ' ' || clientId === null) {
            message_info({'Error de seleccion': 'Favor selecciona un cliente'})
        } else {
            let action = {'action': 'search_client_id', 'id': clientId}
            assets.list(action);
        }
    })

    $('#btnSearchAll').on('click', function () {
        let action = {'action': 'search_client_all'}
        assets.list(action);
    })
});
