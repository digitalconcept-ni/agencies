var client = {
    config: [
        {
            targets: '_all',
            class: 'text-center'
        },
        {
            targets: [0],
            render: function (data, type, row) {
                return `<span class="badge bg-success">${data}</span>`
            }
        },
        {
            targets: [1],
            orderable: false,
            render: function (data, type, row) {
                if (data === true) {
                    return `<span class="badge bg-success p-2 rounded"> </span>`
                } else {
                    return `<span class="badge bg-danger p-2 rounded"> </span>`
                }
            }
        },
        {
            targets: [8],
            orderable: false,
            render: function (data, type, row) {
                return `<span class="m-0" style="border-radius: 0.3rem;   background-color: #d2d6de;border: 1px solid #d2d6de;
            color: #444;margin: 5px 0 0 50px;padding: 5px 10px;"> <b>${data}</b></span>`;
                // var buttons = '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                // buttons += '<a rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                // return buttons;
            }
        },
        {
            targets: [9],
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
            'th': ['NO', 'Estado', 'Vendedor', 'Nombres', 'Número de cédula', 'Fecha de nacimiento', 'Sexo', 'Dirección', 'Visita', 'Opciones'],
            'table': 'tableList',
            'config': client.config,
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

        if (clientId === '' || clientId === null) {
            message_info({'Error de seleccion': 'Favor selecciona un cliente'})
        } else {
            let action = {'action': 'search_client_id', 'id': clientId}
            client.list(action);
        }
    })

    $('#btnSearchAll').on('click', function () {
        let action = {'action': 'search_client_all'}
        client.list(action);
    })
});
