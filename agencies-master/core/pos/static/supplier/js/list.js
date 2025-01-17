var supplier = {
    config: [
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var buttons = `<div class="btn-group" role="group" aria-label="Opciones">`
                buttons += `<a class="btn btn-warning btn-sm" href="${pathname}update/${row[0]}/"><i class="bi bi-pencil-square"></i></a>`;
                buttons += `<a rel="delete" class="btn btn-danger btn-sm"><i class="bi bi-trash3"></i></a></div>`
                return buttons;
            }
        },
    ],
    list: function () {


        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['Nro', 'Nombre', 'Número de telefono', 'Correo', 'Responsable', 'Opciones'],
            'table': 'tableList',
            'config': supplier.config,
            'modal': false,
        }
        drawTables(data);

    }
};

$(function () {
    supplier.list();
});
