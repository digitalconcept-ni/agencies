var specifications = {
    config: [
        {
            targets: '_all',
            class: 'text-center',
        },
        {
            targets: [0],
            visible: false,
        },

        {
            targets: [3, 4, 5],
            orderable: false,
            render: function (data, type, row) {
                var button = `<a href="${data}" target="_blank" type="button" class="btn btn-danger btn-sm" ><i class="bi bi-file-earmark-pdf"></i></a>`;
                if (data === 'No insertado') {
                    var button = `<a href="#" type="button" class="btn btn-danger btn-sm disabled"><i class="bi-file-earmark-pdf"></i></a>`
                    return button
                }
                return button;
            },
        },
        {
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                 var buttons = `<div class="btn-group" role="group" aria-label="Opciones">`
                    buttons += '<a rel="QRcode" class="btn btn-dark btn-sm"><i class="bi bi-qr-code"></i></a> ';
                    buttons += `<a class="btn btn-warning btn-sm" href="${pathname}update/${row[0]}/"><i class="bi bi-pencil-square"></i></a>`;
                    buttons += '<a rel="delete" class="btn btn-danger btn-sm"><i class="bi bi-trash3"></i></a> ';
                buttons += `</div>`;
                return buttons;
            }
        },
    ],
    list: function () {

        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['Nro', 'Nro Lote', 'Fecha produccion', 'Certificado sanitario', 'Características', 'Análisis químico', 'Opciones'],
            'table': 'tableList',
            'config': this.config,
            'modal': false,
        }
        drawTables(data);
    }
};

$(function () {
    specifications.list();

    // Optenemos el contenedor del QR
    // que se encuentra en el modal
    const contenedorQR = document.getElementById('contenedorQR');
    // Inicializamos la variable del generador con el contenedor
    const QR = new QRCode(contenedorQR);

    $('#tableList tbody')
        .on('click', 'a[rel="QRcode"]', function () {
            var tr = tableData.cell($(this).closest('td, li')).index();
            var data = tableData.row(tr.row).data();

            // makeCode utilizafa para generar un nueov qr con los valores que requerimos
            QR.makeCode(`${window.origin}/qrspecifications/${data[1]}`);

            $('#ModalQRcode').modal('show');
        })
});