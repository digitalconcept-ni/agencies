var tblShopping;
var input_daterange;

var sale = {
    config: [
        {
            targets: [0],
            class: 'text-center',
            render: function (data, type, row) {
                if (row[9][1] === true) {
                    return '<a class="badge badge-success badge-pill pointer" rel="number">' + data + '</a>'
                } else {
                    return '<a class="badge badge-danger badge-pill pointer" rel="number">' + data + '</a>'
                }
            }
        },
        {
            targets: [6, 7, 8],
            class: 'text-center',
            render: function (data, type, row) {
                return parseFloat(data).toFixed(2);
            }
        },
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                    buttons += '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                if (data[0] === false) {
                    buttons += '<a href="' + pathname + 'update/' + row[0] + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                }
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
            'th': ['Nro', 'Usuario', 'Proveedor', 'Numero de factura', 'Items', 'Registro', 'Sub total', 'Iva', 'Total', 'Opciones'],
            'table': 'tableList',
            'config': sale.config,
            'modal': false,
        }
        drawTables(data);

        // tblShopping = $('#data').DataTable({
        //     responsive: true,
        //     // scrollX: true,
        //     autoWidth: true,
        //     destroy: true,
        //     deferRender: true,
        //     ajax: {
        //         url: pathname,
        //         type: 'POST',
        //         data: parameters,
        //         dataSrc: "",
        //         headers: {
        //             'X-CSRFToken': csrftoken
        //         }
        //     },
        //     columns: [
        //         {"data": "number"},
        //         {"data": "username"},
        //         {"data": "supplier"},
        //         {"data": "invoice_number"},
        //         {"data": "cant"},
        //         {"data": "date_joined"},
        //         {"data": "subtotal"},
        //         {"data": "iva"},
        //         {"data": "total_iva"},
        //         {"data": "total"},
        //         {"data": "id"},
        //     ],
        //     order: [[0, "desc"], [5, "desc"]],
        //     columnDefs: [
        //         {
        //             targets: [0],
        //             class: 'text-center',
        //             render: function (data, type, row) {
        //                 return '<a class="badge badge-secondary badge-pill pointer" rel="number">' + data + '</a>'
        //             }
        //         },
        //         {
        //             targets: [6, 7, 8, 9],
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
        //                 var buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
        //                 if (row.modify === false) {
        //                     buttons += '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
        //                     buttons += '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
        //                 }
        //                 return buttons;
        //             }
        //         },
        //     ],
        //     initComplete: function (settings, json) {
        //
        //     }
        // });
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
            html += '<td>' + value.product.category.name + '</td>'
            html += '<td>' + value.price + '</td>'
            html += '<td>' + value.cant + '</td>'
            html += '<td>' + value.subtotal + '</td>'
            html += '</tr>';
        });
        html += '</tbody>';
        return html;
    },
    listInvoice: function () {
        let invoice_number = $('input[name="invoice-number"]').val()

        var parameters = {
            'action': 'search_invoice_number',
            'invoice': invoice_number
        };
        tblShopping = $('#data').DataTable({
            responsive: true,
            // scrollX: true,
            // autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: parameters,
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            columns: [
                {"data": "number"},
                {"data": "supplier"},
                {"data": "invoice_number"},
                {"data": "cant"},
                {"data": "date_joined"},
                {"data": "subtotal"},
                {"data": "iva"},
                {"data": "total_iva"},
                {"data": "total"},
                {"data": "id"},
            ],
            order: [[0, "desc"], [2, "desc"]],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a class="badge badge-secondary badge-pill pointer" rel="number">' + data + '</a>'
                    }
                },
                {
                    targets: [-2, -3, -4, -5],
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
                        var buttons = '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                        buttons += '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
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

    $('.btnInvoice').on('click', function () {
        sale.listInvoice();
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
                    {"data": "product.name"},
                    {"data": "product.category.name"},
                    {"data": "price"},
                    {"data": "cant"},
                    {"data": "available"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [0, 1, 2, 3, 4, 5],
                        class: 'text-center',
                    },
                    {
                        targets: [-1, -4],
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });
            $('#myModalProducts').modal('show');
        })
        .on('click', 'a[rel="number"]', function () {
            var tr = $(this).closest('tr');
            var row = tableData.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(sale.formatRowHtml(row.data())).show();
                tr.addClass('shown');
            }
        });

    sale.list(false);
});