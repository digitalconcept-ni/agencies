var input_daterange;

var vehicles = {
    config: [
        {
            targets: [0, 1, 2, 3, 4, 5],
            class: 'text-center'
        }, {
            targets: [0],
            visible: false,
        },
        {
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                buttons += '<a href="' + pathname + 'update/' + row[0] + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                return buttons;
            }
        },
    ],
    list: function () {

        let data = {
            'data': {'action': 'search',},
            'inserInto': 'rowList',
            'th': ['id', 'Vehiculo', 'Conductor', 'Nro Placa', 'Fecha registro', 'Opciones'],
            'table': 'tableList',
            'config': this.config,
            'modal': false,
        }
        drawTables(data);
    },
    formatRowHtml: function (d) {
        var html = '<table class="table">';
        html += '<thead class="thead-dark">';
        html += '<tr><th scope="col">Producto</th>';
        html += '<th scope="col">Categoría</th>';
        html += '<th scope="col">PVP</th>';
        html += '<th scope="col">Cantidad</th>';
        html += '<th scope="col">Subtotal</th></tr>';
        html += '</thead>';
        html += '<tbody>';
        $.each(d.saleproduct, function (key, value) {
            html += '<tr>'
            html += '<td>' + value.product.name + '</td>'
            html += '<td>' + value.product.brand + '</td>'
            html += '<td>' + value.price + '</td>'
            html += '<td>' + value.cant + '</td>'
            html += '<td>' + value.subtotal + '</td>'
            html += '</tr>';
        });
        html += '</tbody>';
        return html;
    }
};

$(function () {

    $('#tableList tbody')
        .off()
        .on('click', 'a[rel="details"]', function () {
            var tr = tableData.cell($(this).closest('td, li')).index();
            var data = tableData.row(tr.row).data();
            $('#tblProducts').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_products_detail',
                        'id': data[0]
                    },
                    dataSrc: "",
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                },
                columns: [
                    {
                        "data": "product"
                    },

                    {
                        "data": "price"
                    },
                    {
                        "data": "cant"
                    },
                    {
                        "data": "subtotal"
                    },
                    {
                        "data": "reason_loss"
                    },
                ],
                columnDefs: [
                    {
                        targets: [0, 1, 2, 3, 4],
                        class: 'text-center',
                    },
                    {
                        targets: [-3],
                        render: function (data) {
                            return parseFloat(data).toFixed(2);
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });
            $('#myModalProducts').modal('show');
        })

    vehicles.list(false);
});