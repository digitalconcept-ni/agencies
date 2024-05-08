var input_daterange;
$(function () {

    input_daterange = $('input[name="date_range_2"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
                applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
                cancelLabel: '<i class="fas fa-times"></i> Cancelar',
            },
        })


    $('#btnSearchSalesxPresaleInfo').on('click', function () {
        var selector = $('#selectPreSales2').val();

        if (selector.length === 0) {
            message_info({'Error de seleccion': 'Favor de seleccionar el preventa'})
        } else {
            var parameters = {
                'action': 'search_sale_presale',
                'presale': selector,
                'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
                'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
            };

            let config = [{
                targets: [-1, -2, -3],
                class: 'text-center',
                orderable: false,
                // render: function (data, type, row) {
                //     return 'C$' + parseFloat(data).toFixed(2);
                // }
            },]
            let data = {
                'data': parameters,
                'inserInto': 'rowData',
                'th': ['Nro', 'Categoria','Marca', 'Producto', 'Cantidad'],
                'table': 'data',
                'config': config,
                'modal': false,
            }
            drawTables(data);

        }
    })

    $('.drp-buttons').hide();
});