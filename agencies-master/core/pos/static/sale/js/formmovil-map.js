var tblProducts;
var select_search_product;
var tblSearchProducts;
// let coordClient = false;

var sale = {
    details: {
        subtotal_exempt: 0.00,
        subtotal: 0.00,
        iva: 0.00,
        discount: 0.00,
        total: 0.00,
        products: [],
        products_review: []
    },
    getProductsIds: function () {
        return this.details.products.map(value => value.id);
    },
    calculateInvoice: function () {
        var subtotal_exempt = 0.00;
        var subtotal_iva = 0.00;
        var discount = $('input[name="discount"]').val();
        this.details.products.forEach(function (value, index, array) {
            value.index = index;

            if (value.tax === 'e' || value.tax === 'exento') {
                value.cant = parseInt(value.cant);
                value.subtotal = value.cant * parseFloat(value.pvp);
                subtotal_exempt += value.subtotal;
            } else if (value.tax === 'grabado') {
                value.cant = parseInt(value.cant);
                value.subtotal = value.cant * parseFloat(value.pvp);
                subtotal_iva += value.subtotal;
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
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
    },
    listProducts: function () {
        this.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: false,
            autoWidth: true,
            destroy: true,
            paging: false,
            dom: 't',
            // scrollY: '58vh',
            scrollCollapse: true,
            data: this.details.products,
            columns: [
                {"data": "id"},
                {"data": "full_name"},
                {"data": "cant"},
                {"data": "pvp"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    visible: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn-xs" style="font-size: 12px; font-weight: bold">' + data + '</a>';
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [3, 4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                // $(row).find('input[name="cant"]').TouchSpin({
                //     min: 1,
                //     max: data.stock === 0 ? data.cant : data.stock + data.cant,
                //     step: 1
                // });

            },
        });
    },
    calculateTotalItems: function () {
    }
};

$(function () {

    select_search_product = $('select[name="search_product"]');

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    select_search_product.select2({
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
                    action: 'search_products_select2',
                    ids: JSON.stringify(sale.getProductsIds())
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar producto (nombre o código)',
        minimumInputLength: 1,
        templateResult: function (repo) {
            if (repo.loading) {
                return repo.text;
            }

            if (!Number.isInteger(repo.id)) {
                return repo.text;
            }
            var tax = '';

            if (repo.tax === 'e' || repo.tax === 'exento') {
                tax = 'Exento';
            } else if (repo.tax === 'g' || repo.tax === 'grabado') {
                tax = 'Grabado'
            }

            var stock = repo.is_inventoried ? repo.stock : 'Sin stock';

            return $(
                '<div class="wrapper container">' +
                '<div class="row">' +
                '<div class="col-lg-1">' +
                '</div>' +
                '<div class="col-lg-11 text-left shadow-sm p-2">' +
                //'<br>' +
                '<p style="margin-bottom: 0;">' +
                '<b>Nombre:</b> ' + repo.full_name + '<br>' +
                '<b>Stock:</b> ' + stock + '<br>' +
                '<b>PVP:</b> <span class="badge bg-primary">' + repo.pvp + '</span>' + '<br>' +
                '<b>Tipo:</b> <span class="badge bg-secondary">' + tax + '</span>' +
                '</p>' +
                '</div>' +
                '</div>' +
                '</div>');
        },
    })
        .on('select2:select', function (e) {
            var data = e.params.data;
            if (!Number.isInteger(data.id)) {
                return false;
            }
            data.cant = 1;
            data.subtotal = 0.00;
            sale.addProduct(data);
            select_search_product.val('').trigger('change.select2');
        });

    $('#tblProducts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    sale.details.products.splice(tr.row, 1);
                    tblProducts.row(tr.row).remove().draw();
                    sale.calculateInvoice();
                }, function () {

                });
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sale.details.products[tr.row].cant = cant;
            sale.calculateInvoice();
            $('td:last', tblProducts.row(tr.row).node()).html('$' + sale.details.products[tr.row].subtotal.toFixed(2));
        });

    $('.btnRemoveAll').on('click', function () {
        if (sale.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            sale.details.products = [];
            sale.listProducts();
        }, function () {

        });
    });

    $('.btnClearSearch').on('click', function () {
        select_search_product.val('').focus();
    });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(sale.getProductsIds()),
                    'term': select_search_product.val()
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                {"data": "full_name"},
                {"data": "image"},
                {"data": "stock"},
                {"data": "pvp"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.is_inventoried) {
                            return '<span class="badge badge-secondary">Sin stock</span>';
                        }
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="add" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var product = tblSearchProducts.row(tr.row).data();
            product.cant = 1;
            product.subtotal = 0.00;
            sale.addProduct(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    // Form Sale

    // $("input[name='iva']").on('change', function () {
    //     sale.calculateInvoice();
    // }).val(0.00);

    $("input[name='discount']").on('change', function () {
        sale.calculateInvoice();
    })

    // $('input[name="latitud"]').on('change', function () {
    //     coordClient = true;
    // })
    // $('input[name="longitud"]').on('change', function () {
    //     coordClient = true;
    // })

    // const btnSendForm = document.getElementById("send-form");
    //
    // btnSendForm.addEventListener("submit", function () {
    //
    // })

    $('#frmSale').on('submit', async function (e) {
        e.preventDefault();

        if (sale.details.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        let products = sale.details.products;
        let products_review = sale.details.products_review;

        if (navigator.onLine) {
            var success_url = this.getAttribute('data-url');
            var parameters = new FormData(this);
            parameters.append('action', 'add_map');
            parameters.append('products', JSON.stringify(products));
            parameters.append('products_review', JSON.stringify(products_review));
            submit_with_ajax(pathname, 'Guaarda',
                '¿Estas seguro de guardar?', parameters, function (response) {
                    // alert_action('Notificación', '¿Desea imprimir la factura de venta?', function () {
                    //     window.open('/pos/sale/invoice/pdf/' + response.id + '/', '_blank');
                    //     location.href = success_url;
                    // }, function () {
                    //     location.href = '/map/client-detail/';
                    // });
                    location.href = '/map/client-detail/';
                });
        } else {
            sessionStorage.getItem('cliente');
        }

    });

    sale.listProducts();
});

