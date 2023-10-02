var tblSale;
var input_daterange;

var sale = {
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
        tblSale = $('#data').DataTable({
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
            columns: [{
                "data": "number"
            },
                {
                    "data": "user"
                },
                {
                    "data": "client.full_name"
                },
                {
                    "data": "date_joined"
                },
                {
                    "data": "subtotal"
                },
                {
                    "data": "iva"
                },
                {
                    "data": "total_iva"
                },
                {
                    "data": "total"
                },
                {
                    "data": "id"
                },
            ],
            order: [
                [0, "desc"],
                [2, "desc"]
            ],
            columnDefs: [{
                targets: [0],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.endofday === true) {
                        return '<a class="badge badge-success badge-pill pointer" rel="number">' + data + '</a>'
                    } else {
                        return '<a class="badge badge-secondary badge-pill pointer" rel="number">' + data + '</a>'
                    }
                }
            },
                {
                    targets: [-2, -3, -4, -5],
                    class: 'text-center',
                    render: function (data) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                        if (row.modify === false) {
                            buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                            buttons += '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        }
                        buttons += '<a href="' + pathname + 'invoice/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
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

    $('#selectPreSales').on('change', function (e) {
        if ($(this).val() !== '') {
            $('#btnDonwloadGuide').removeClass('disabled');
        } else {
            $('#btnDonwloadGuide').addClass('disabled');
        }
    })

    $('#btnDonwloadGuide').on('click', function (e) {
        id = $('#selectPreSales').val()
        let param = {
            'action': 'download_guides',
            'id': id
        }
        if (id !== '') {
            let loader = document.querySelector('.preloader-container');
            loader.style.opacity = 1
            loader.style.visibility = 'initial'
            $.ajax({
                url: pathname,
                data: param,
                type: 'POST',
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (request) {
                    loader.style.opacity = 0
                    loader.style.visibility = 'hidden'
                    if (!request.hasOwnProperty('error')) {
                        if (request.hasOwnProperty('info')) {
                            message_info(request)
                        } else {
                            console.log(request)
                            document.getElementById('iconDonwload').href = request.path
                            $('#iconDonwload').removeClass('disabled')

                            return false;
                        }
                    } else {
                        message_error(request.error);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    message_error(errorThrown + ' ' + textStatus);
                }
            });
        }
    })

    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        sale.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        sale.list(true);
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="details"]', function () {
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
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
                        'id': data.id
                    },
                    dataSrc: "",
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                },
                columns: [{
                    "data": "product.name"
                },
                    {
                        "data": "product.category.name"
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
                ],
                columnDefs: [{
                    targets: [-1, -3],
                    class: 'text-center',
                    render: function (data) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                    {
                        targets: [-2],
                        class: 'text-center',
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
            var row = tblSale.row(tr);
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