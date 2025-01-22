var assets = {
    config: [
        {
            targets: '_all',
            class: 'text-center'
        },
        {
            targets: [0],
            visible: false,
        },
        {
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                var buttons = `
                <div class="btn-group" role="group" aria-label="Opciones">
                <a class="btn btn-warning" href="${pathname}update/${row[0]}/"><i class="bi bi-pencil-square"></i></a>
                <a rel="delete" class="btn btn-danger"><i class="bi bi-trash3"></i></a>
              </div>`
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
