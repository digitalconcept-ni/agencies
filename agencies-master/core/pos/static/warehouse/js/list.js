var tblShopping;
var input_daterange;

var warehouse = {
    config: [
        {
            targets: '_all',
            class: 'text-center'
        },
        {
            targets: [-2],
            orderable: false,
            render: function (data, type, row) {
                return `<span class="m-0" style="border-radius: 0.3rem;   background-color: #d2d6de;border: 1px solid #d2d6de
            color: #444;margin: 5px 0 0 50px;padding: 5px 10px;"> <b>${data}</b></span>`;

            }
        },
        {
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                var buttons = `<div class="btn-group" role="group" aria-label="Opciones">`
                buttons += `<a rel="details" class="btn btn-primary btn-sm"><i class="bi bi-search"></i></a>`
                buttons += `<a class="btn btn-warning btn-sm" href="${pathname}update/${row[0]}/"><i class="bi bi-pencil-square"></i></a>`;
                // buttons += `<a rel="delete" class="btn btn-danger btn-sm"><i class="bi bi-trash3"></i></a></div>`
                return buttons;

            }
        },
    ],
    list: function (all) {

        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['ID', 'Codigo', 'Nombre', '¿Es central?', 'Descripción', 'Estato', 'Usuarios permitidos', 'Opciones'],
            'table': 'tableList',
            'config': this.config,
            'modal': false,
        }
        drawTables(data);

    },
    formatRowHtml: function (d) {
        var html = '<table class="table">';
        html += '<thead class="thead-dark">';
        html += '<th scope="col">Cantidad</th>';
        html += '<th scope="col">Categoría</th>';
        html += '<tr><th scope="col">Producto</th>';
        html += '<th scope="col">Costo</th>';
        html += '<th scope="col">Subtotal</th></tr>';
        html += '</thead>';
        html += '<tbody>';
        $.each(d.warehouseproduct, function (key, value) {
            html += '<tr>'
            html += '<td>' + value.cant + '</td>'
            html += '<td>' + value.product.category.name + '</td>'
            html += '<td>' + value.product.name + '</td>'
            html += '<td>' + value.price + '</td>'
            html += '<td>' + value.subtotal + '</td>'
            html += '</tr>';
        });
        html += '</tbody>';
        return html;
    },
};

$(function () {


    $('#tableList tbody')
        .off()
        .on('click', 'a[rel="details"]', function (e) {
            var tr = $('#tableList').DataTable().cell($(this).closest('td, li')).index();
            var warehouseID = $('#tableList').DataTable().row(tr.row).data();

            let config = [
                {
                    targets: '_all',
                    class: 'text-center',
                },
            ]
            let data = {
                'data': {'action': 'search_products_detail', 'warehouse_id': warehouseID[0]},
                'inserInto': 'rowModalInfo',
                'th': ['Producto', 'Stock'],
                'table': 'tableModalInfo',
                'config': config,
                'modal': true,
            }
            drawTables(data);

            // $('#tblProducts').DataTable({
            //     responsive: true,
            //     autoWidth: false,
            //     destroy: true,
            //     deferRender: true,
            //     //data: data.det,
            //     ajax: {
            //         url: pathname,
            //         type: 'POST',
            //         data: {
            //             'action': 'search_products_detail',
            //             'id': data[0]
            //         },
            //         dataSrc: "",
            //         headers: {
            //             'X-CSRFToken': csrftoken
            //         },
            //     },
            //     columns: [
            //         {"data": "product"},
            //         {"data": "stock"},
            //     ],
            //     columnDefs: [
            //         {
            //             targets: '_all',
            //             class: 'text-center',
            //         },
            //
            //     ],
            // });
            // $('#myModalProducts').modal('show');
        })
        .on('click', 'a[rel="number"]', function () {
            var tr = $(this).closest('tr');
            var row = tableData.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(warehouse.formatRowHtml(row.data())).show();
                tr.addClass('shown');
            }
        });

    warehouse.list(false);
});