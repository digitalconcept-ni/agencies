var input_daterange;

var loss = {
    config: [
        {
            targets: [0, 1, 2, 3, 4, 5],
            class: 'text-center'
        },
        {
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                buttons += '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                // if (row[12][0] === false) {
                //     buttons += '<a href="' + pathname + 'update/' + row[0] + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                // }
                // buttons += '<a href="' + pathname + 'invoice/pdf/' + row[0] + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                return buttons;
            }
        },
    ],
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }

        let data = {
            'data': parameters,
            'inserInto': 'rowList',
            'th': ['Lote', 'Creado por', 'Fecha registro', 'Hora registro', 'Total perdida', 'Opciones'],
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

    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        sale.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        sale.list(true);
    });

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

    loss.list(false);
});