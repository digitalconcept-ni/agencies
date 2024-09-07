var input_daterange;
var productStatus;

var production = {
    config: [
        {
            targets: [0, 1, 2, 3, 4, 5, 6, 7],
            class: 'text-center',
        },
        {
            targets: [1],
            render: function (data, type, row) {
                if (data === false) {
                    return `<a class="badge badge-danger badge-pill pointer" rel="status">Proceso</a>`
                } else {
                    return `<a class="badge badge-success badge-pill">Completo</a>`
                }
            },
        },
        {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a rel="rawMaterial" class="btn btn-info btn-xs btn-flat"><i class="fas fa-hammer"></i></a> ';
                buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                // if (row[12][0] === false) {
                //     buttons += '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                // }
                buttons += '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                if (row[1] === false) {
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
            'th': ['Lote', 'Estatus', 'Creado por', 'Fecha registro', 'Fecha proceso', 'Fin de Proceso', 'Eficiencia', 'Opciones'],
            'table': 'tableList',
            'config': this.config,
            'modal': false,
        }
        drawTables(data);
    },
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
        production.list(false);
    });

    $('.btnSearchAll').on('click', function () {
        production.list(true);
    });

    $('#modalStatus').on('hidden.bs.modal', function (e) {
        $('#frmProductStatus').trigger('reset');
    });

    $('#tableList tbody')
        .off()
        .on('click', 'a[rel="details"]', function () {
            var tr = tableData.cell($(this).closest('td, li')).index();
            var data = tableData.row(tr.row).data();
            if (data[1] == false) {
                $('#btnFinallyProduction').css('display', 'block');
            } else {
                $('#btnFinallyProduction').css('display', 'none');

            }
            tableProducts = $('#tblProducts').DataTable({
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
                        "data": "product_id"
                    },
                    {
                        "data": "category"
                    },
                    {
                        "data": "product"
                    },

                    {
                        "data": "cant"
                    },
                ],
                columnDefs: [
                    {
                        targets: [0, 1, 2, 3],
                        class: 'text-center',
                    },
                    {
                        targets: [0],
                        visible: false,
                    },
                    {
                        targets: [3],
                        render: function (row) {
                            if (data[1] == false) {
                                return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row + '">';
                            } else {
                                return row
                            }
                        }
                    },
                ],
                rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                    $(row).find('input[name="cant"]').TouchSpin({
                        min: 1,
                        max: 100000,
                        step: 1
                    });

                },
                initComplete: function (settings, json) {
                    productStatus = json
                }
            });
            $('#myModalProducts').modal('show');
        })
        .on('click', 'a[rel="rawMaterial"]', function () {
            var tr = tableData.cell($(this).closest('td, li')).index();
            var data = tableData.row(tr.row).data();

            tableRawMaterials = $('#tblRowMaterials').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_raw_materials',
                        'id': data[0]
                    },
                    dataSrc: "",
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                },
                columns: [
                    {"data": "id"},
                    {"data": "supplier"},
                    {"data": "product"},
                    {"data": "price"},
                    {"data": "cant"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [0, 1, 2, 3, 4, 5],
                        class: 'text-center',
                    },
                    {
                        targets: [0],
                        visible: false,
                    },
                    {
                        targets: [3],
                        render: function (data, type, row) {
                            if (data === '') {
                                return '---------'
                            } else {
                                return parseFloat(data).toFixed(2)
                            }
                        }
                    },
                    {
                        targets: [5],
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(2)
                        }
                    }
                ],
            })
            $('#modalRawMaterials').modal('show');
        })

    $('#tblProducts tbody').on('change', 'input[name="cant"]', function (e) {
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tableProducts.cell($(this).closest('td, li')).index();
        productStatus[tr.row].cant = cant;
    });

    $('#btnFinallyProduction').on('click', function (e) {
        var parameters = new FormData();
        parameters.append('action', 'change_status');
        parameters.append('products', JSON.stringify(productStatus));
        submit_with_ajax(pathname, '¿Estás seguro de finalizar el proceso?',
            'La siguiente acción modificara el inventario actual', parameters, function (response) {
                //console.log(response);
                $('#tableList').DataTable().ajax.reload();
                $('#myModalProducts').modal('hide');

            });
    });

    production.list(false);
});