$(function () {
    $('#btnSearchPresaleInfo').on('click', function () {
        console.log('follow')
        var Selector = $('#selectPreSales').val();

        if (Selector !== '') {
            var id = Selector;
            let config = [
                {
                    targets: [3, 4],
                    class: 'text-center',
                },
                {
                    targets: [0],
                    visible: false
                },
                {
                    targets: [1],
                    class: 'text-center',
                },
                {
                    targets: [2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return 'C$ ' + parseFloat(data).toFixed(2);
                    }
                },
            ]
            let data = {
                'data': {'action': 'search_presale_info', 'id': id},
                'inserInto': 'rowData',
                'th': ['Nro', 'Cantidad de facturas', 'Total C$', 'Ultimo Cliente', 'Hora ultimo pedido'],
                'table': 'data',
                'config': config,
                'modal': false,
            }
            console.log(data)
            drawTables(data);
        }
    })

})

