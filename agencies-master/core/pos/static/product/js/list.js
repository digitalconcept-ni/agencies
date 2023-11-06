var product = {
    config: [
        {
            targets: [0],
            visible: false,
        },
        {
            targets: [3],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                return '<img alt="" src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
            }
        },
        {
            targets: [4],
            class: 'text-center',
            render: function (data, type, row) {
                if (data) {
                    return '<span class="badge badge-success">Si</span>';
                }
                return '<span class="badge badge-warning">No</span>';
            }
        },
        {
            targets: [5],
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
            targets: [6, 7],
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
            'th': ['Nro', 'Nombre', 'Categoria', 'Imagen', '¿Es inventariado?', 'Stock', 'Costo', 'Precio venta', 'Opciones'],
            'table': 'tableList',
            'config': product.config,
            'modal': false,
        }
        drawTables(data);

        // tblProduct = $('#data').DataTable({
        //     responsive: true,
        //     autoWidth: false,
        //     destroy: true,
        //     deferRender: true,
        //     ajax: {
        //         url: pathname,
        //         type: 'POST',
        //         data: {
        //             'action': 'search'
        //         },
        //         dataSrc: "",
        //         headers: {
        //             'X-CSRFToken': csrftoken
        //         }
        //     },
        //     columns: [
        //         {"data": "id"},
        //         {"data": "full_name"},
        //         {"data": "category.name"},
        //         {"data": "image"},
        //         {"data": "is_inventoried"},
        //         {"data": "stock"},
        //         {"data": "cost"},
        //         {"data": "pvp"},
        //         {"data": "id"},
        //     ],
        //     columnDefs: [
        //         {
        //             targets: [3],
        //             class: 'text-center',
        //             orderable: false,
        //             render: function (data, type, row) {
        //                 return '<img alt="" src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
        //             }
        //         },
        //         {
        //             targets: [4],
        //             class: 'text-center',
        //             render: function (data, type, row) {
        //                 if (row.is_inventoried) {
        //                     return '<span class="badge badge-success">Si</span>';
        //                 }
        //                 return '<span class="badge badge-warning">No</span>';
        //             }
        //         },
        //         {
        //             targets: [5],
        //             class: 'text-center',
        //             render: function (data, type, row) {
        //                 if (!row.is_inventoried) {
        //                     return '<span class="badge badge-secondary">Sin stock</span>';
        //                 }
        //                 if (row.stock > 0) {
        //                     return '<span class="badge badge-success">' + data + '</span>';
        //                 }
        //                 return '<span class="badge badge-danger">' + data + '</span>';
        //             }
        //         },
        //         {
        //             targets: [-2],
        //             class: 'text-center',
        //             render: function (data, type, row) {
        //                 return '$' + parseFloat(data).toFixed(2);
        //             }
        //         },
        //         {
        //             targets: [-1],
        //             class: 'text-center',
        //             orderable: false,
        //             render: function (data, type, row) {
        //                 var buttons = '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
        //                 buttons += '<a rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
        //                 return buttons;
        //             }
        //         },
        //     ],
        //     initComplete: function (settings, json) {
        //
        //     }
        // });
    }
};

$(function () {
    product.list();
});
