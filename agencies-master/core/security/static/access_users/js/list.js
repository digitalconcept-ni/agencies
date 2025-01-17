var input_daterange;

var access_users = {
    config: [
        {
            targets: [0],
            visible: false,
        },
        {
            targets: [-2],
            class: 'text-center',
            render: function (data, type, row) {
                if (data['id'] === 'success') {
                    return `<button type="button" class="btn btn-success btn-sm"><i class="bi bi-check-circle"></i></button>`;
                }
                return `<button type="button" class="btn btn-danger btn-sm"><i class="bi-exclamation-octagon"></i></button`;

            }
        },
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                return `<a rel="delete" type="button" class="btn btn-danger btn-sm"><i class="bi bi-trash3"></i></a>`
                // return `<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="bi bi-trash3"></i></a>`;
            }
        },
    ],
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }

        let data = {
            'data': parameters,
            'inserInto': 'rowList',
            'th': ['Nro', 'Usuario', 'Registro', 'Direccion IP', 'Coordenadas', 'Exactitud', 'Intento', 'Opciones'],
            'table': 'tableList',
            'config': access_users.config,
            'modal': false,
        }

        drawTables(data);
    },
};

$(function () {

    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        access_users.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        access_users.list(true);
    });

    access_users.list(false);
});