var info = {
    callInfo: function () {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'search_data'},
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
        }).done(function (data) {
            $.each(data, v => {
                $(`#${v}`).text(data[v])
            });

            $("#tableDashProductSold").DataTable({
                deferRender: true,
                responsive: true,
                autoWidth: false,
                destroy: true,
                orderable: false,
                data: data.maximumsold,
                dom: 'Bfrtip',
                // order: false,
                paging: false,
                ordering: false,
                info: false,
                searching: false,
                buttons: [
                    {
                        extend: 'excelHtml5',
                        text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                        titleAttr: 'Excel',
                        className: 'btn btn-success btn-flat'
                    }],
                columnDefs: [
                    {
                        targets: [0, 2],
                        class: 'text-center',
                    },

                ]
            });
        })
    }
};

$(function () {
    info.callInfo();

    const ProductSoldToday = () => {
        let config = [
            {
                targets: [0],
                class: 'text-center',
                visible: false
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.stock > 6) {
                        return '<span class="badge badge-success">' + data + '</span>';
                    } else if (row.stock === 0) {
                        return '<span class="badge badge-secondary">Sin stock</span>';
                    } else {
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }
                }
            },
            {
                targets: [4],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ]
        let data = {
            'data': {'action': 'search_lower_inventory'},
            'inserInto': 'rowModal',
            'th': ['id', 'Nombre', 'Categoria', 'Stock', 'Costo'],
            'table': 'tableModal',
            'config': config,
            'modal': true,
        }
        drawTables(data);
    }
    setInterval(function () {
        info.callInfo()
    }, 15000)

    $('#lower').on('click', function () {

        let config = [
            {
                targets: [0],
                class: 'text-center',
                visible: false
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.stock > 6) {
                        return '<span class="badge badge-success">' + data + '</span>';
                    } else if (row.stock === 0) {
                        return '<span class="badge badge-secondary">Sin stock</span>';
                    } else {
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }
                }
            },
            {
                targets: [4],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ]
        let data = {
            'data': {'action': 'search_lower_inventory'},
            'inserInto': 'rowModal',
            'th': ['id', 'Nombre', 'Categoria', 'Stock', 'Costo'],
            'table': 'tableModal',
            'config': config,
            'modal': true,
        }
        drawTables(data);
    })

    $('#btn-sale-products').on('click', function () {
        $('#myModalLowerInvetory').modal('hide');

    })

    // Funcion para poder ver los costos y ganancias del inventario
    $('#pro').on('click', function () {

        let config = [
            {
                targets: [1, 2],
                class: 'text-center',
                render: function (data, type, row) {
                    return 'C$ ' + parseFloat(data).toFixed(2);
                }
            },
        ]
        let data = {
            'data': {'action': 'search_investment'},
            'inserInto': 'rowModal',
            'th': ['Nro', 'Inversión', 'Ganancia'],
            'table': 'tableModal',
            'config': config,
            'modal': true,
        }
        drawTables(data);
    })

    $('#salestoday').on('click', function () {
        let header = `<h3 class="card-title"><i class="fas fa-info-circle"> </i> Seguimiento</h3>`
        let data = {
            'modalHeaderBody': header,
        }
        drawModal(data)
    })

    // $('#selectPreSales').on('change', function () {
    //     if ($(this).val() !== '') {
    //         var id = $(this).val();
    //         let config = [
    //             {
    //                 targets: [0],
    //                 visible: false
    //             },
    //             {
    //                 targets: [1],
    //                 class: 'text-center',
    //             },
    //             {
    //                 targets: [2],
    //                 class: 'text-center',
    //                 render: function (data, type, row) {
    //                     return 'C$ ' + parseFloat(data).toFixed(2);
    //                 }
    //             },
    //         ]
    //         let data = {
    //             'data': {'action': 'search_presale_info', 'id': id},
    //             'inserInto': 'rowDash',
    //             'th': ['Nro', 'Cantidad de facturas', 'Total C$', 'Ultimo Cliente', 'Hora ultimo pedido'],
    //             'table': 'tableDash',
    //             'config': config,
    //             'modal': false,
    //         }
    //         drawTables(data);
    //     }
    // })

})