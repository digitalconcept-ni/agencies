var tblProducts;
var select_search_product;
var tblSearchProducts;
var action = $('input[name="action"]').val();


var loss = {
    details: {
        total: 0.00,
        products: [],
        products_review: []
    },
    getProductsIds: function () {
        return this.details.products.map(value => value.id);
    },
    calculateInvoice: function () {
        var subtotal = 0.00;
        this.details.products.forEach(function (value, index, array) {
            value.index = index;
            value.cant = parseInt(value.cant);
            value.subtotal = value.cant * parseFloat(value.cost);
            subtotal += value.subtotal;
        });

        this.details.total = subtotal

        $('input[name="total"]').val(this.details.total.toFixed(2));
    },
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
    },
    listProducts: function () {
        var action = $('input[name="action"]').val();
        this.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            columns: [
                {"data": "id"},
                {"data": "full_name"},
                {"data": "cost"},
                {"data": "cant"},
                {"data": "subtotal"},
                {"data": "razon"},
            ],
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center',
                },
                {
                    targets: [0],
                    visible: false,
                },
                {
                    targets: [1],
                    render: function (data, type, row) {
                        return '<a rel="remove" style="color: blue; cursor: pointer">' + data + '</a>';
                    }
                },
                {
                    targets: [2],
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [4],
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [3],
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + 1 + '">';
                    }
                },
                {
                    targets: [-1],
                    render: function (data, type, row) {
                        return `<textarea style="resize: none;" class="form-control" name="razon" id="razon" cols="50" rows="3" placeholder="Describe el porqué"></textarea>`
                    }
                },
            ],

        });
    },
};

$(function () {

    select_client = $('select[name="client"]');
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
                    ids: JSON.stringify(loss.getProductsIds())
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
        templateResult: function (repo) {
            if (repo.loading) {
                return repo.text;
            }

            if (!Number.isInteger(repo.id)) {
                return repo.text;
            }

            var stock = repo.is_inventoried ? repo.stock : 'Sin stock';

            var tax = '';

            if (repo.tax === 'e' || repo.tax === 'exento') {
                tax = 'Exento';
            } else if (repo.tax === 'g' || repo.tax === 'grabado') {
                tax = 'Grabado'
            }
            return $(
                '<div class="wrapper container">' +
                '<div class="row">' +
                // '<div class="col-lg-1">' +
                // '<img alt="" src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                // '</div>' +
                '<div class="col-lg-11 text-left shadow-sm">' +
                //'<br>' +
                '<p style="margin-bottom: 0;">' +
                '<b>Nombre:</b> ' + repo.full_name + '<br>' +
                '<b>Stock:</b> ' + stock + '<br>' +
                '<b>PVP:</b> <span class="badge badge-warning">$' + repo.pvp + '</span>' + '<br>' +
                '<b>Tipo:</b> <span class="badge badge-dark">' + tax + '</span>' +
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
            loss.addProduct(data);
            select_search_product.val('').trigger('change.select2');
        });

    $('#tblProducts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    loss.details.products.splice(tr.row, 1);
                    tblProducts.row(tr.row).remove().draw();
                    loss.calculateInvoice();
                }, function () {

                });
        })
        .on('change', 'input[name="cant"]', function () {
            // console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            loss.details.products[tr.row].cant = cant;
            loss.calculateInvoice();
            $('td:nth-last-child(2)', tblProducts.row(tr.row).node()).html(loss.details.products[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'textarea[name="razon"]', function () {
            var r = $(this).val();
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            loss.details.products[tr.row].razon = r;
        })

    $('#btnRemoveAll').on('click', function () {
        if (loss.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            loss.details.products = [];
            loss.listProducts();
        }, function () {

        });
    });

    $('.btnClearSearch').on('click', function () {
        select_search_product.val('').focus();
    });

    // Form loss

    $('#frmloss').on('submit', function (e) {
        e.preventDefault();

        if (loss.details.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('total', $('input[name="total"]').val());
        parameters.append('products', JSON.stringify(loss.details.products));
        parameters.append('products_review', JSON.stringify(loss.details.products_review));
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                location.href = success_url;
            });
    });

    loss.listProducts();
});

