var technicians = {
    config: [
        // {
        //     targets: [0],
        //     visible: false,
        // },
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a href="' + pathname + 'update/' + row[0] + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                buttons += '<a rel="delete" button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                return buttons;
            }
        },
    ],
    list: function () {

        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['Nro', 'Nombres', 'Puesto', 'Creado por', 'Fecha creación', 'Opciones'],
            'table': 'tableList',
            'config': technicians.config,
            'modal': false,
        }
        drawTables(data);
    }
};

$(function () {
    technicians.list();

    $('.btnAdd').on('click', function (e) {
        $('#modalTechnicians').modal('show')
    })

    $('#modalTechnicians').on('shown.bs.modal', function (e) {
        $('form').trigger('reset');
    })

    tableData.on('click', 'input[rel="restore"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            let tr = tblProducts.cell($(this).closest('td, li')).index();
            const _this = $(this);

            if (_this.prop('checked')) {
                sale.details.products[tr.row].restore = true
                let s = 0.00
                $('td:last', tblProducts.row(tr.row).node()).html(s.toFixed(2));

            } else {
                sale.details.products[tr.row].restore = false
                $('td:last', tblProducts.row(tr.row).node()).html(sale.details.products[tr.row].subtotal.toFixed(2));

            }
            sale.calculateInvoice();
        })

    $('form').on('submit', function (e) {
        e.preventDefault();

        var param = new FormData(this);
        submit_with_ajax(pathname, 'Notificacion', '¿Estás seguro de la siguiente acción?', param, function () {

            $('form').trigger('reset');
            $('#modalTechnicians').modal('hide')
            tableData.ajax.reload();
        });
    })
});