var product = {
    config: [
        {
            targets: [0],
            visible: false,
        },
        // {
        //     targets: [4],
        //     class: 'text-center',
        //     orderable: false,
        //     render: function (data, type, row) {
        //         return '<img alt="" src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
        //     }
        // },
        {
            targets: [5],
            class: 'text-center',
            render: function (data, type, row) {
                if (data) {
                    return '<span class="badge badge-success">Si</span>';
                }
                return '<span class="badge badge-warning">No</span>';
            }
        },
        {
            targets: [6],
            class: 'text-center',
            render: function (data, type, row) {
                if (data === 0) {
                    return '<span class="badge badge-secondary">Sin stock</span>';
                } else if (data > 10) {
                    return '<span class="badge badge-success">' + data + '</span>';
                }
                return '<span class="badge badge-danger">' + data + '</span>';
            }
        },
        {
            targets: [7, 8],
            class: 'text-center',
            render: function (data, type, row) {
                return 'C$' + parseFloat(data).toFixed(2);
            }
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
        },
    ],
    list: function () {

        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['Nro', 'Categoría', 'Nombre', 'Vencimiento', 'Impuesto', '¿Es inventariado?', 'Stock', 'Costo', 'Precio venta', 'Opciones'],
            'table': 'tableList',
            'config': product.config,
            'modal': false,
        }
        drawTables(data);
    }
};

$(function () {
    product.list();
});
