var sale = {
    details: {
        subtotal_exempt: 0.00,
        subtotal: 0.00,
        iva: 0.00,
        discount: 0.00,
        total: 0.00,
    },
    products: [],
    products_delete: [],
    getProductsIds: function () {
        return this.products.map(value => value.id);
    },
    addProduct: function (item) {
        this.products.push(item);
    },
    calculateInvoice: function () {
        var subtotal_exempt = 0.00;
        var subtotal_iva = 0.00;
        // var iva = $('input[name="iva"]').val();
        var discount = $('input[name="discount"]').val();
        this.products.forEach(function (value, index) {
            value.index = index;
            value.cant = parseInt(value.cant);
            value.subtotal = value.cant * parseFloat(value.pvp_list[`${value.applied_price}`]);
            // value.subtotal = value.cant * parseFloat(value.pvp);

            if (!value.restore) {
                if (value.tax === 'e' || value.tax === 'exento') {
                    subtotal_exempt += value.subtotal;
                } else if (value.tax === 'grabado') {
                    subtotal_iva += value.subtotal;
                }
            }
        });

        this.details.subtotal_exempt = subtotal_exempt;
        this.details.subtotal = subtotal_iva;
        this.details.discount = discount;

        this.details.iva = this.details.subtotal * 0.15;
        this.details.total = ((this.details.subtotal + this.details.subtotal_exempt) - this.details.discount) + this.details.iva;

        $('input[name="subtotal"]').val(this.details.subtotal.toFixed(2));
        $('input[name="subtotal_exempt"]').val(this.details.subtotal_exempt.toFixed(2));
        $('input[name="ivacalc"]').val(this.details.iva.toFixed(2));
        $('input[name="total"]').val(this.details.total.toFixed(2));
    },
};

$(function () {
    var action = $('input[name="action"]').val();

    $('.select2').select2({
        theme: "bootstrap4",
    });

    // $("input[name='discount']").TouchSpin({
    //     min: 0,
    //     max: 1000000,
    //     step: 0.01,
    //     decimals: 2,
    //     boostat: 5,
    //     maxboostedstep: 10,
    //     // postfix: 'C$'
    // }).on('change', function () {
    //     sale.calculateInvoice();
    // })

    $('#frmSale').on('submit', function (e) {
        e.preventDefault();

        if (sale.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        // if (action == 'add') {
        //     if (!coordClient) {
        //         message_error('Favor de Geo localizar al cliente');
        //         return false;
        //     }
        // }


        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('details', JSON.stringify(sale.details));
        parameters.append('products', JSON.stringify(sale.products));
        if (action === 'edit') {
            parameters.append('products_delete', JSON.stringify(sale.products_delete));
        }

        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                alert_action('Notificación', '¿Desea imprimir la factura de venta?', function () {
                    window.open('/pos/sale/invoice/pdf/' + response.id + '/', '_blank');
                    location.href = success_url;
                }, function () {
                    location.href = success_url;
                });
            });
    });

    const calculateCanceled = () => {
        let today = $('#id_days').val()
        let end = $('#id_end')
        let date = new Date().getTime() + (today * 24 * 60 * 60 * 1000);
        let f = new Date(date).toLocaleDateString().split('/').reverse();
        let canceledDate = f.join('-');
        end.val(canceledDate)
    }

    if ($('#id_payment').val() === 'credit') {
        $('#block-credit').css('display', 'flex');
    }

    $('#id_payment').on('change', function () {
        let _this = $(this).val();

        if (_this === 'credit') {
            $('#block-credit').css('display', 'flex');
            calculateCanceled()
        } else {
            $('#block-credit').css('display', 'none');
        }
    })


    $('#id_days').on('change', function () {
        calculateCanceled()

    })

    $('input[type="checkbox"]').on('change', function () {
        let frequent = $('#id_frequent').prop('checked');
        let is_active = $('#id_is_active').prop('checked');

        if ((frequent && !is_active) && this.checked) {
            message_error({'Error de seleccion': 'Favor de desmarcar frecuente si tendrá días específicos de visita'})
        } else if (frequent && this.checked) {
            message_error({'Error de seleccion': 'Favor de desmarcar frecuente si tendrá días específicos de visita'})
        }
    });
});

