var product = {
    config: [
        {
            targets: [0, 1, 2],
            visible: false,
        },
        {
            targets: '_all',
            class: 'text-center',
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
            targets: [6],
            render: function (data, type, row) {
                if (data) {
                    return `<span class="badge bg-success"><i class="bi bi-check-circle me-1"></i>Si</span>`
                }
                return `<span class="badge bg-warning text-dark"><i class="bi bi-exclamation-triangle me-1"></i>No</span>`

            }
        },
        // {
        //     targets: [7],
        //     render: function (data, type, row) {
        //         if (data === 0) {
        //             return `<span class="badge bg-danger"><i class="bi bi-exclamation-octagon me-1"></i>Sin stock</span>`
        //         } else if (data > 10) {
        //             return `<span class="badge bg-success"><i class="bi bi-check-circle me-1"></i>${data}</span>`
        //         }
        //         return `<span class="badge bg-warning text-dark"><i class="bi bi-exclamation-triangle me-1"></i>${data}</span>`
        //     }
        // },
        // {
        //     targets: [7, 8],
        //     render: function (data, type, row) {
        //         return  parseFloat(data).toFixed(2);
        //     }
        // },
        {
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                var buttons = `
                <div class="btn-group" role="group" aria-label="Opciones">
                <a class="btn btn-warning btn-sm" href="${pathname}update/${row[0]}/"><i class="bi bi-pencil-square"></i></a>
                <a rel="delete" class="btn btn-danger btn-sm"><i class="bi bi-trash3"></i></a>
              </div>`
                return buttons;
            }
        },
    ],
    list: function () {

        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['Nro', 'Marca', 'Categoría', 'Nombre', 'Vencimiento', 'Impuesto', '¿Es inventariado?', 'Costo', 'Precio venta #1', 'Precio venta #2', 'Precio venta #3', 'Opciones'],
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
