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
                // dom: 'Bfrtip',
                // order: false,
                paging: false,
                ordering: false,
                info: false,
                searching: false,
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

    // const ProductSoldToday = () => {
    //     let config = [
    //         {
    //             targets: [0],
    //             class: 'text-center',
    //             visible: false
    //         },
    //         {
    //             targets: [3],
    //             class: 'text-center',
    //             render: function (data, type, row) {
    //                 if (row.stock > 6) {
    //                     return '<span class="badge badge-success">' + data + '</span>';
    //                 } else if (row.stock === 0) {
    //                     return '<span class="badge badge-secondary">Sin stock</span>';
    //                 } else {
    //                     return '<span class="badge badge-danger">' + data + '</span>';
    //                 }
    //             }
    //         },
    //         {
    //             targets: [4],
    //             class: 'text-center',
    //             render: function (data, type, row) {
    //                 return '$' + parseFloat(data).toFixed(2);
    //             }
    //         },
    //     ]
    //     let data = {
    //         'data': {'action': 'search_lower_inventory'},
    //         'inserInto': 'rowModal',
    //         'th': ['id', 'Nombre', 'Categoria', 'Stock', 'Costo'],
    //         'table': 'tableModal',
    //         'config': config,
    //         'modal': true,
    //     }
    //     drawTables(data);
    // }

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
                visible: false,
                // render: function (data, type, row) {
                //     return '$' + parseFloat(data).toFixed(2);
                // }
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

    $('#sale').on('click', function () {
        let config = [
            {
                targets: [0],
                visible: false,
            },
            {
                targets: [1, 2, 3, 4],
                class: 'text-center',
                render: function (data, type, row) {
                    var html = `<div class="row">
                        <div class="col-12">
                            <span class="badge bg-success" style="font-size: 14px">${data[0]}</span>
                        </div>
                        <div class="col-12">
                            <span>C$ ${parseFloat(data[1]).toFixed(2)}</span>
                        </div>
                    </div>`
                    // return `<span class="badge bg-success">${data[0]}</span> - C$ ${parseFloat(data[1]).toFixed(2)}`;
                    // return 'C$ ' + parseFloat(data).toFixed(2);
                    return html;
                }
            },
        ]
        let data = {
            'data': {'action': 'search_payment_method'},
            'inserInto': 'rowModal',
            'th': ['Nro', 'Efectivo', 'POS', 'Transferencia', 'Credito'],
            'table': 'tableModal',
            'config': config,
            'modal': true,
        }
        drawTables(data);
    })

    $('#programingClients').on('click', function () {

        let config = [
            {
                targets: [0],
                visible: false
            },
            {
                targets: [1, 2, 3, 4],
                class: 'text-center',
            },
            {
                targets: [4],
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(2);
                }
            },]
        let data = {
            'data': {'action': 'search_presale_info'},
            'inserInto': 'rowModal',
            'th': ['Nro', 'Preventa', 'Clientes Programados', 'Clientes Efectivos', 'Efectividad'],
            'table': 'tableModal',
            'config': config,
            'modal': true,
        }
        drawTables(data);
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