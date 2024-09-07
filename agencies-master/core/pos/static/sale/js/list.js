var input_daterange;

var sale = {
    config: [
        {
            targets: [0],
            class: 'text-center',
            render: function (data, type, row) {
                if (row[12][1] === true) {
                    return '<a class="badge badge-success badge-pill pointer" rel="number">' + data + '</a>'
                } else {
                    return '<a class="badge badge-secondary badge-pill pointer" rel="number">' + data + '</a>'
                }
            }
        },
        {
            targets: [2],
            class: 'text-center',
            render: function (data, type, row) {
                if (data === 'cash') {
                    return '<a class="badge badge-success badge-pill" rel="number">' + data + '</a>'
                } else if (data === 'credit') {
                    if (row[12][2] === true) {
                        return '<a class="badge badge-success badge-pill">' + data + '</a>';
                    } else {
                        return '<a class="badge badge-danger badge-pill pointer" rel="credit">' + data + '</a>'
                    }
                } else if (data === 'transfer') {
                    return '<a class="badge badge-dark badge-pill" rel="number">' + data + '</a>'
                } else if (data === 'pos') {
                    return '<a class="badge badge-info badge-pill" rel="number">' + data + '</a>'
                }
            }
        },
        {
            targets: [7, 8, 9],
            class: 'text-center',
            render: function (data) {
                return 'C$' + parseFloat(data).toFixed(2);
            }
        },
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                if (row[12][0] === false) {
                    buttons += '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="' + pathname + 'update/' + row[0] + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                }
                buttons += '<a href="' + pathname + 'invoice/pdf/' + row[0] + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
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
            'th': ['Nro', 'Cliente', 'Pago', 'Orden de compra', 'Creado por', 'Venta de', 'Registro', 'Sub Total Exento', 'Sub total IVA', 'Descuento', 'Iva', 'Total', 'Opciones'],
            'table': 'tableList',
            'config': sale.config,
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


    // variables que seleccionar los select donde pondremos las horas del preventa
    let startHour = $('#selectRangeHourStart');
    let endHour = $('#selectRangeHourEnd');

    $('#selectPreSales').on('change', function (e) {
        let _this = $(this);

        if (_this.val() !== '') {
            var param = new FormData();
            param.append('action', 'search_time');
            param.append('id', _this.val());

            $.ajax({
                url: pathname,
                data: param,
                type: 'POST',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                processData: false,
                contentType: false,
                success: function (request) {
                    if (!request.hasOwnProperty('error')) {
                        startHour.empty()
                        endHour.empty()
                        var opt = '';

                        $.each(request, function (key, value) {
                            opt += `<option value="${value[0]}">${value[1]}</option>`;
                        });
                        startHour.append(opt);
                        endHour.append(opt);
                        $('#btnDonwloadGuide').removeClass('disabled');
                        return false;
                    } else {
                        message_error(request.error);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    message_error(errorThrown + ' ' + textStatus);
                }
            });
        } else {
            $('#btnDonwloadGuide').addClass('disabled');
        }
    })

    $('#btnDonwloadGuide').on('click', function (e) {
        id = $('#selectPreSales').val();
        var param = new FormData();

        if (startHour.val() !== endHour.val()) {
            param.append('startHour', startHour.val());
            param.append('endHour', endHour.val());
        }

        if (id !== '') {
            param.append('action', 'download_guides');
            param.append('session', $('#idSession').prop('checked'));
            param.append('id', id);

            submit_with_ajax(pathname, 'Descargar Guia', '¿Estas seguro de esta accion?', param, function (request) {
                if (request.hasOwnProperty('info')) {
                    message_info(request.info)
                } else {
                    document.getElementById('iconDonwload').href = request.path
                    $('#iconDonwload').removeClass('disabled')
                        .removeClass('d-none')
                        .css('display', 'inline-block');
                    tableData.ajax.reload();
                    Swal.fire({
                        title: 'Alerta',
                        text: 'Guia realizada correctamente',
                        icon: 'success',
                        timer: 1500,
                    })
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
                        "data": "product.name"
                    },
                    {
                        "data": "product.brand.name"
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
                columnDefs: [
                    {
                        targets: [0, 1, 2, 3],
                        class: 'text-center',
                    },
                    {
                        targets: [0],
                       render: function (data, type, row){
                            if(row.restore){
                                return `<span style="color: red">${data}</span>`
                            }else{
                                return data
                            }

                       }
                    },
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data) {
                            return parseFloat(data).toFixed(2);
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
        .on('click', 'a[rel="credit"]', function () {
            var tr = tableData.cell($(this).closest('td, li')).index();
            var row = tableData.row(tr.row).data();
            var param = new FormData();
            param.append('action', 'apply_credit')
            param.append('id', row[0])

            submit_with_ajax(pathname, '¿Seguro de aplicar la factura?', 'Esta factura estará aplicada en sistema como pagada',
                param, function () {
                    Swal.fire({
                        position: "top-end",
                        icon: "success",
                        title: "La factura ha sido aplicada correctamente",
                        showConfirmButton: false,
                        timer: 1800
                    });
                })
        });
    ;

    sale.list(false);
});