var select_client;

var sale = {
    details: {
        subtotal_exempt: 0.00,
        subtotal: 0.00,
        iva: 0.00,
        discount: 0.00,
        total: 0.00,
        products: [],
        products_delete: [],
    },
    calculateInvoice: function () {
        var subtotal_exempt = 0.00;
        var subtotal_iva = 0.00;
        // var iva = $('input[name="iva"]').val();
        var discount = $('input[name="discount"]').val();
        this.details.products.forEach(function (value, index, array) {
            value.index = index;
            if (!value.restore) {
                if (value.tax === 'e' || value.tax === 'exento') {
                    value.cant = parseInt(value.cant);
                    value.subtotal = value.cant * parseFloat(value.pvp);
                    subtotal_exempt += value.subtotal;
                } else if (value.tax === 'grabado') {
                    value.cant = parseInt(value.cant);
                    value.subtotal = value.cant * parseFloat(value.pvp);
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

    select_client = $('select[name="client"]');
    select_search_product = $('select[name="search_product"]');

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // Client

    select_client.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_client'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            var data = e.params.data;

            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {'action': 'search_if_exits_client', 'id_client': data.id},
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            }).done(function (data) {
                if (data.exists) {
                    Swal.fire({
                        title: "Notificación",
                        text: "El cliente seleccionado ya cuenta con una venta",
                        icon: "warning",
                        confirmButtonColor: "#3085d6",
                        confirmButtonText: "Ok!"
                    }).then((result) => {
                        if (result.isConfirmed) {
                            location.href = data.success_url;
                        }
                    });
                }
                // else {
                //     var lat = e.params.data.lat;
                //     console.log(lat)
                //     if (lat != null || lat != undefined) {
                //         coordClient = true;
                //     } else {
                //         coordClient = false;
                //     }
                // }

            })
        });

    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function (e) {
        $('#frmClient').trigger('reset');
    });

    $('#frmClient').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente Cliente?', parameters, function (response) {
                //console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                select_client.append(newOption).trigger('change');
                $('#myModalClient').modal('hide');
            });
    });

    $("input[name='discount']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        // postfix: 'C$'
    }).on('change', function () {
        sale.calculateInvoice();
    })

    $('#frmSale').on('submit', function (e) {
        e.preventDefault();

        if (sale.details.products.length === 0) {
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

        // parameters.append('coords', false);
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

    $('input[type="checkbox"]').on('change', function (e) {
        let frequent = $('#id_frequent').prop('checked');
        let is_active = $('#id_is_active').prop('checked');

        if ((frequent && !is_active) && this.checked) {
            message_error({'Error de seleccion': 'Favor de desmarcar frecuente si tendrá días específicos de visita'})
        } else if (frequent && this.checked) {
            message_error({'Error de seleccion': 'Favor de desmarcar frecuente si tendrá días específicos de visita'})
        }
    });
});

