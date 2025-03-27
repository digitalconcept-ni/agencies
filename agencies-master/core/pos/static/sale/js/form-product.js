var tblProducts;
var select_search_product, tblSearchProducts;

var product = {
    getProductsIds: function () {
        return sale.details.products.map(value => value.id);
    },
    addProduct: function (item) {
        sale.details.products.push(item);
        this.listProducts();
    },
    listProducts: function () {
        let action = $('input[name="action"]').val();
        sale.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: sale.details.products,
            columns: [
                {"data": "id"},
                {"data": "restore"},
                {"data": "full_name"},
                {"data": "stock"},
                {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
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
                        var check = ` <div class="form-check form-switch">`
                        if (action === 'edit') {
                            if (row.before === true) {
                                if (data === false) {
                                    check += '<input class="form-check-input" type="checkbox"  rel="restore">'
                                } else {
                                    check += '<input class="form-check-input" type="checkbox"  rel="restore" checked>'
                                }
                            } else {
                                check += '<input class="form-check-input" type="checkbox" disabled>'
                            }
                        } else if (action === 'add') {
                            check += '<input class="form-check-input" type="checkbox"  rel="restore" disabled>'
                        }
                        check += `</div>`
                        return check;

                    }
                },
                {
                    targets: [2],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" style="color: blue; cursor: pointer">' + data + '</a>';
                    }
                },
                {
                    targets: [-4],
                    orderable: false,
                    render: function (data, type, row) {
                        if (!row.is_inventoried) {
                            return `<span class="badge bg-secondary">Sin stock</span>`
                        }
                        return `<span class="badge bg-secondary">${data}</span>`
                    }
                },
                {
                    targets: [-3],
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.restore === true) {
                            return '<input disabled type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cant + '">';
                        } else {
                            return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cant + '">';
                        }
                    }
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
            ],
        });
    },
};

$(function () {
    var action = $('input[name="action"]').val();

    select_search_product = $('select[name="search_product"]');

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
                    ids: JSON.stringify(product.getProductsIds())
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
                '<b>PVP:</b> <span class="badge bg-secondary">' + repo.pvp + '</span>' + '<br>' +
                '<b>Tipo:</b> <span class="badge bg-dark">' + tax + '</span>' +
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
            product.addProduct(data);
            select_search_product.val('').trigger('change.select2');
        });

    $('#tblProducts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function (e) {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    let delItem = sale.details.products.splice(tr.row, 1);
                    delItem[0].delete = true;
                    sale.details.products_delete.push(delItem);
                    product.listProducts();
                });
        })
        .on('change', 'input[name="cant"]', function (e) {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            if (action === 'edit') {
                if (sale.details.products[tr.row].hasOwnProperty('before') &&
                    !sale.details.products[tr.row].hasOwnProperty('initial_amount')) {
                    sale.details.products[tr.row]['initial_amount'] = sale.details.products[tr.row][e.target.name];
                }
            }

            sale.details.products[tr.row].cant = cant;
            sale.calculateInvoice();
            $('td:last', tblProducts.row(tr.row).node()).html(sale.details.products[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'input[rel="restore"]', function (e) {
            // console.clear();
            var cant = parseInt($(this).val());
            let tr = tblProducts.cell($(this).closest('td, li')).index();
            const _this = $(this);
            // Seleccionar el input con name="cant" en la misma fila
            let cantInput = _this.closest('tr').find('input[name="cant"]');

            if (_this.prop('checked')) {
                if (sale.details.products[tr.row].hasOwnProperty('before')) {
                    sale.details.products[tr.row].restore = true
                }
                // Deshabilitar el input
                cantInput.prop('disabled', true);

                let s = 0.00
                $('td:last', tblProducts.row(tr.row).node()).html(s.toFixed(2));

            } else {
                sale.details.products[tr.row].restore = false
                console.log(typeof sale.details.products[tr.row].subtotal)
                console.log(sale.details.products[tr.row].subtotal)

                let s = parseFloat(sale.details.products[tr.row].cant) * parseFloat(sale.details.products[tr.row].pvp);
                $('td:last', tblProducts.row(tr.row).node()).html(s.toFixed(2));

                // Deshabilitar el input
                cantInput.prop('disabled', false);

            }
            sale.calculateInvoice();
        })

    $('.btnRemoveAll').on('click', function () {
        if (sale.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            sale.details.products = [];
            sale.listProducts();
        }, function () {

        });
    });

    product.listProducts();


})