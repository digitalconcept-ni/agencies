var warehouse = {
    details: {
        subtotal: 0.00, // Sub total con descueto
        discount: 0.00,
        iva: 0.00,
        income_tax: 0.00, // 2% IMPUESTO SOBRE LA RENTA
        city_tax: 0.00, // 1% IMPUESTO MUNICIPAL
        total: 0.00,
        products: [],
        products_delete: [],
        calc: {
            iva: true,
            income_tax: false,
            city_tax: false,
        }
    },
};

$(function () {

    var action = $('input[name="action"]').val();

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // Verificando los valores de los impuesto

    if (action === 'edit') {
        // Cambiamos la clase del tbn y el icono
        $.each($('.btn-calc'), function (index, item) {
            var buttonId = $(item).attr('id');
            var inputValue = $(`#id_${buttonId}`).val();

            console.log(inputValue)
            // Verificamos si el valor es mayor que 0.00
            if (inputValue > 0.00) {
                // Si el botón no tiene la clase btn-success, la agregamos
                if (!$(item).hasClass('btn-success')) {
                    $(item).addClass('btn-success').removeClass('btn-danger')
                        .find('.bi').removeClass('bi-ban').addClass('bi-check-circle');
                    warehouse.details.calc[`${buttonId}`] = true; // Establecer en true
                } else {
                    // Si ya tiene la clase btn-success, mantenemos el valor en true
                    warehouse.details.calc[`${buttonId}`] = true;
                }
            } else {
                // Si el valor es menor o igual a 0.00, cambiamos a btn-danger
                $(item).addClass('btn-danger').removeClass('btn-success')
                    .find('.bi').removeClass('bi-check-circle').addClass('bi-ban');
                warehouse.details.calc[`${buttonId}`] = false; // Establecer en false
            }
        })
    }


    $('#frmwarehouse').on('submit', function (e) {
        e.preventDefault();

        // if (warehouse.details.products.length === 0) {
        //     message_error('Debe al menos tener un item en su detalle en su compra');
        //     return false;
        // }

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('products', JSON.stringify(warehouse.details.products));
        if (action === 'edit') {
            parameters.append('products_delete', JSON.stringify(warehouse.details.products_delete));
        }
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                location.href = success_url;
            });
    });

});

