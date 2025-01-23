var tblProducts;
var select_client, select_search_product, select_search_shopping;
var tblSearchProducts;

var production = {
    details: {
        totalShopping: 0.00,
        shopping: [],
        shopping_delete: [],
        products: [],
    },
    calculateInvoice: function () {
        var sub = 0.00
        this.details.shopping.forEach(function (value, index, array) {
            value.index = index;

            value.cant = parseInt(value.cant);
            value.subtotal = value.cant * parseFloat(value.price);
            sub += value.subtotal;
        });

        this.details.totalShopping = sub;

        $('input[name="totalShopping"]').val(this.details.totalShopping.toFixed(2));
    },
    getShoppingIds: function () {
        return this.details.shopping.map(value => value.id_shopping);
    },
    getProductsIds: function () {
        return this.details.products.map(value => value.id);
    },
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
    },
    addShop: function (item) {
        this.details.shopping.push(item);
        this.listShopping();
    },
    listProducts: function () {
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            columns: [
                {"data": "id"},
                {"data": "full_name"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    visible: false,
                    // render: function (data, type, row) {
                    //     return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    // }
                },
                {
                    targets: [1],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" style="color: blue; cursor: pointer">' + data + '</a>';
                    }
                },

                // {
                //     targets: [2],
                //     class: 'text-center',
                //     orderable: false,
                //     render: function (data, type, row) {
                //         return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                //     }
                // },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000,
                    step: 1
                });

            },
        });
    },
    listShopping: function () {
        this.calculateInvoice();
        tblShopping = $('#tblSearchShoppings').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.shopping,
            columns: [
                {"data": "id_shopping"},
                {"data": "shopping_name"},
                {"data": "id_product"},
                {"data": "product_name"},
                {"data": "price"},
                {"data": "available"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0, 2],
                    visible: false,
                },
                {
                    targets: [0, 1, 2, 3, 4, 5, 6, 7],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [1],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" style="color: blue; cursor: pointer">' + data + '</a>';
                    }
                },
                {
                    targets: [6],
                    render: function (data, type, row) {
                        return `<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="${row.product}">`;
                    }
                },
                {
                    targets: [-1],
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2)
                    }
                }
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: data.available == 0 ? data.cant : data.available,
                    step: 1
                });

            },
        });
    },

};

$(function () {
    let action = $('input[name="action"]').val()

    select_search_product = $('select[name="search_product"]');
    select_search_shopping = $('select[name="search_shopping"]');

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // *****************************
    // FUNCTIONALITY FOR SHOPPING

    // Funcion que nos ayudara a buscar las facturas que requiera el cliente
    // para saber cuanto cuesta la produccion

    $('.btnSearchShoppings').on('click', function () {
        $('#myModalSearchShoppings').modal('show');
    });
    // Buscardor de las facturas de compras
    select_search_shopping.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        dropdownParent: $('#myModalSearchShoppings'),
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
                    action: 'search_shoppings',
                    ids: JSON.stringify(production.getShoppingIds())
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese Nro factura o proveedor',
        minimumInputLength: 1,
        templateResult: function (repo) {
            if (repo.loading) {
                return repo.text;
            }

            if (!Number.isInteger(repo.id)) {
                return repo.text;
            }

            return $(
                `<div class="wrapper container">
                    <div class="row">
                        <div class="col-lg-11 text-left shadow-sm">
                            <p style="margin-bottom: 0;">
                                <b>Nro factura: </b>${repo.value}<br>
                                <b>Fecha factura: </b>${repo.date_joined}<br>
                                <b>Ingresada por: </b>${repo.username}<br>
                            </p>
                        </div>
                    </div>
                </div>`
            );
        },
    })
        .on('select2:select', function (e) {
            var data = e.params.data;

            if (!Number.isInteger(data.id)) {
                return false;
            }

            // Seleccionamos los datos que requerimos para almacenarlos
            var products = data.shopping_details;
            $.each(products, function (index, value) {
                if (value.available !== 0) {
                    let insert = {}
                    insert['id_shopping'] = data.id
                    insert['shopping_name'] = data.value
                    insert['id_product'] = value.product.id
                    insert['product_name'] = value.product.full_name
                    insert['price'] = value.price
                    insert['available'] = value.available
                    insert['cant'] = 1
                    insert['subtotal'] = 0.00
                    production.addShop(insert)
                }
            })
            select_search_shopping.val('').trigger('change.select2');
        });

    $('#tblSearchShoppings tbody')
        .off()
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblShopping.cell($(this).closest('td, li')).index();
            if (action === 'edit') {
                if (!production.details.shopping[tr.row].hasOwnProperty('before_cant')) {
                    production.details.shopping[tr.row]['before_cant'] = production.details.shopping[tr.row].cant;
                }
            }
            production.details.shopping[tr.row].cant = cant;

            production.calculateInvoice();
            $('td:nth-last-child(1)', tblShopping.row(tr.row).node()).html(production.details.shopping[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblShopping.cell($(this).closest('td, li')).index();
            var delItem = production.details.shopping.splice(tr.row, 1);
            production.details.shopping_delete.push(delItem[0]);
            tblShopping.row(tr.row).remove().draw();
            production.calculateInvoice();

        })


    // FIN LOGICA DE LISTA DE FACTURAS
    // *******************************


    // Funcion para buscar los productos con select2
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
                    ids: JSON.stringify(production.getProductsIds())
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
                '<b>Stock:</b> ' + repo.stock + '<br>' +
                '<b>Categoria:</b> <span class="badge badge-dark">' + repo.category.name + '</span>' +
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
            insert = {'id': data.id, 'full_name': data.full_name};
            production.addProduct(insert);
            select_search_product.val('').trigger('change.select2');
        });

    $('#tblProducts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    production.details.products.splice(tr.row, 1);
                    tblProducts.row(tr.row).remove().draw();
                }, function () {

                });
        })

    $('.btnRemoveAll').on('click', function () {
        if (production.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            production.details.products = [];
            production.listProducts();
        }, function () {

        });
    });

    $('.btnClearSearch').on('click', function () {
        select_search_product.val('').focus();
    });

    // Form production

    $('#frmproduction').on('submit', function (e) {
        e.preventDefault();

        if (production.details.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        if (production.details.shopping.length === 0) {
            message_error('Debe al menos tener una factura ingresada de compra de materia prima');
            return false;
        }

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        if (action == 'edit') {
            parameters.append('products_review', JSON.stringify(production.details.products_review));
            parameters.append('shopping_delete', JSON.stringify(production.details.shopping_delete));
        }
        parameters.append('products', JSON.stringify(production.details.products));
        parameters.append('shopping', JSON.stringify(production.details.shopping));
        submit_with_ajax(pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = success_url;
        });
    });

    production.listProducts();
    production.listShopping();
});

