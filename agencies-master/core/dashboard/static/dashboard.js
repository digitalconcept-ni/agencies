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
                // Se integra este conficonal para validad los datos de produccion
                if (v === 'prod') {
                    $.each(data[v], function (k, c) {
                        $(`#${k}`).text(c)
                    })
                } else {
                    $(`#${v}`).text(data[v])
                }
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

    setInterval(function () {
        info.callInfo()
    }, 20000)

    $('#lower').on('click', function () {

        let config = [
            {
                targets: [0, 3, 4, 5, 7, 8, 9],
                class: 'text-center',
                visible: false
            },
            {
                targets: [6],
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
            'th': ['Nro', 'Marca', 'Nombre', 'Vencimiento', 'Imagen', '¿Es inventariado?', 'Stock', 'Costo', 'Precio venta', 'Opciones'],
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

    $('#pending-invoices').on('click', function () {

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
            'data': {'action': 'view-credit-noapplied'},
            'inserInto': 'rowModal',
            'th': ['Nro', 'Orden de compra', 'Usuario', 'Cliente', 'Cancelacion', 'Monto'],
            'table': 'tableModal',
            'config': [],
            'modal': true,
        }
        drawTables(data);
    })

})