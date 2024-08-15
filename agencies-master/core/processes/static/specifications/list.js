var specifications = {
    config: [
        {
            targets: [1, 2, 3, 4, 5, 6],
            class: 'text-center',
        },
        {
            targets: [0],
            visible: false,
        },

        {
            targets: [3],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var button = '<a href="' + row[3] + '" target="_blank" type="button" class="btn btn-danger" ><i class="fas fa-file-pdf"></i></a>';
                if (row[3] === 'No insertado') {
                    var button = '<a href="#" type="button" class="btn btn-danger disabled"><i class="far fa-file-pdf"></i></a>'
                    return button
                }
                return button;
            },
        },
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var buttons = `<a rel="QRcode" type="button" class="btn btn-dark btn-xs btn-flat mr-1"><i class="fas fa-qrcode"></i></a>`
                buttons += `<a href="${pathname}update/${row[0]}/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a>`
                buttons += `<a rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>`
                return buttons;
            }
        },
    ],
    list: function () {

        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['Nro','Nro Lote' ,'Fecha produccion', 'Certificado sanitario', 'Características', 'Análisis químico', 'Opciones'],
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