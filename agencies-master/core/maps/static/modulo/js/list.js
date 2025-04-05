var zone = {
    config: [
        {
            targets: [0],
            visible: false,
        },
        {
            targets: '_all',
            class: 'text-center',
        },
        {
            targets: [-1],
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
            'th': ['Nro', 'Ruta', 'Código', 'Ubigeo', 'Limites', 'Opciones'],
            'table': 'tableList',
            'config': zone.config,
            'modal': false,
        }
        drawTables(data);
    }
};

$(function () {
    zone.list();
});
