var shopping = {
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
    calculateInvoice: function () {

        let discount = $('input[name="discount"]').val();
        let iva = $('input[name="iva"]');
        let income_tax = $('input[name="income_tax"]');
        let city_tax = $('input[name="city_tax"]');
        let subtotal = 0.00;

        this.details.products.forEach(function (value, index) {
            value.cant = parseInt(value.cant);
            value.subtotal = parseFloat(value.cant * parseFloat(value.cost));
            subtotal += parseFloat(value.subtotal)
        });

        this.details.discount = parseFloat(discount);
        this.details.subtotal = subtotal - this.details.discount;

        // calculo de los impuestos
        this.details.iva = this.details.calc.iva ? this.details.subtotal * 0.15 : 0.00;
        this.details.income_tax = this.details.calc.income_tax ? this.details.subtotal * 0.02 : 0.00;
        this.details.city_tax = this.details.calc.city_tax ? this.details.subtotal * 0.01 : 0.00;

        this.details.total = parseFloat(this.details.subtotal) + parseFloat(this.details.iva) +
            parseFloat(this.details.income_tax) + parseFloat(this.details.city_tax);

        $('input[name="subtotal"]').val(formatNumber(this.details.subtotal));
        iva.val(formatNumber(this.details.iva));
        income_tax.val(this.details.income_tax.toFixed(2));
        city_tax.val(this.details.city_tax.toFixed(2));
        $('input[name="total"]').val(formatNumber(this.details.total));
    },
};

$(function () {

    var action = $('input[name="action"]').val();

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $("input[name='discount']").on('change', function () {
        if ($(this).val() === '') {
            $(this).val(0.00)
        }
        shopping.calculateInvoice();
    })

    // Funcion para saber que btn esta seleccionado el usuairo
    // y saber si calculara el: IVA, IR, IM

    $('.btn-calc').on('click', function () {
        let _this = $(this)
        // Obtener el ID del botón que fue clicado
        var buttonId = _this.attr('id');

        // Cambiamos la clase del tbn y el icono
        _this.toggleClass('btn-danger btn-success')
            .find('.bi').toggleClass('bi-check-circle bi-ban')

        if (_this.hasClass('btn-danger')) {
            shopping.details.calc[`${buttonId}`] = false;
        }
        if (_this.hasClass('btn-success')) {
            shopping.details.calc[`${buttonId}`] = true;
        }

        shopping.calculateInvoice();

    });

    // Verificando los valores de los impuesto

    if (action === 'edit') {
        // Cambiamos la clase del tbn y el icono
        $.each($('.btn-calc'), function (index, item) {
            var buttonId = $(item).attr('id');
            var inputValue = $(`#id_${buttonId}`).val();

            // Verificamos si el valor es mayor que 0.00
            if (inputValue > 0.00) {
                // Si el botón no tiene la clase btn-success, la agregamos
                if (!$(item).hasClass('btn-success')) {
                    $(item).addClass('btn-success').removeClass('btn-danger')
                        .find('.bi').removeClass('bi-ban').addClass('bi-check-circle');
                    shopping.details.calc[`${buttonId}`] = true; // Establecer en true
                } else {
                    // Si ya tiene la clase btn-success, mantenemos el valor en true
                    shopping.details.calc[`${buttonId}`] = true;
                }
            } else {
                // Si el valor es menor o igual a 0.00, cambiamos a btn-danger
                $(item).addClass('btn-danger').removeClass('btn-success')
                    .find('.bi').removeClass('bi-check-circle').addClass('bi-ban');
                shopping.details.calc[`${buttonId}`] = false; // Establecer en false
            }
        })
    }


    $('#frmshopping').on('submit', function (e) {
        e.preventDefault();

        if (shopping.details.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle en su compra');
            return false;
        }

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('details', JSON.stringify(shopping.details));
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                location.href = success_url;
            });
    });

});

