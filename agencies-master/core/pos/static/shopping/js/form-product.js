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

        sale.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: sale.details.products,
            columns: [
                {"data": "id"},
                {"data": "cant"},
                {"data": "full_name"},
                {"data": "expiration"},
                {"data": "cost"},
                {"data": "pvp"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    visible: false
                },
                {
                    targets: '_all',
                    class: 'text-center',
                },
                {
                    targets: [2],
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn-xs" style="font-size: 14px; font-weight: bold">' + data + '</a>';
                    }
                },
                {
                    targets: [3],
                    render: function (data, type, row) {
                        // El minimo de fecha de vencimiento sera el dia del ingreso de la factura a sistema

                        // Obtener la fecha actual
                        const today = new Date();

                        // Formatear la fecha en el formato YYYY-MM-DD
                        const year = today.getFullYear();
                        const month = String(today.getMonth() + 1).padStart(2, '0'); // Los meses son 0-indexados
                        const day = String(today.getDate()).padStart(2, '0');
                        const formattedDate = `${year}-${month}-${day}`;

                        return `<input  type="date" name="expiration" min="${formattedDate}" id="expiration" class="form-control form-control-sm"/>`;
                    }
                },
                {
                    targets: [4],
                    orderable: false,
                    render: function (data, type, row) {
                        // return '$' + parseFloat(data).toFixed(2);
                        return '<input type="text" name="cost" class="form-control form-control-sm" autocomplete="off" value="' + parseFloat(data).toFixed(2) + '">';
                    }
                },
                {
                    targets: [5],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="pvp" class="form-control form-control-sm" autocomplete="off" value="' + parseFloat(data).toFixed(2) + '">';
                    }
                },
                {
                    targets: [1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [6],
                    orderable: false,
                    render: function (data, type, row) {
                        return formatNumber(data);
                    }
                },],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                // $(row).find('input[name="cant"]').TouchSpin({
                //     min: 1,
                //     max: 1000000,
                //     step: 1
                // });
                // $(row).find('input[name="cost"]').TouchSpin({
                //     min: 0.01,
                //     max: 1000000,
                //     step: 0.01,
                //     decimals: 2,
                //     boostat: 5,
                //     maxboostedstep: 10,
                // });
                // $(row).find('input[name="pvp"]').TouchSpin({
                //     min: 0.01,
                //     max: 1000000,
                //     step: 0.01,
                //     decimals: 2,
                //     boostat: 5,
                //     maxboostedstep: 10,
                // });

            },
        });
    },
};

$(function () {
    var action = $('input[name="action"]').val();

    select_search_product = $('select[name="search_product"]');

    // Event to open the modal to create a new product
    $('.btnCreateProduct').on('click', function () {
        $('#myModalCreateProduct').modal('show');
    });


    $('#myModalCreateProduct').on('hidden.bs.modal', function (e) {
        $('#frmCreateProduct').trigger('reset');
    });


    // Event form to create a new Product
    $('#frmCreateProduct').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_new_product');
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente producto?', parameters, function (response) {
                //console.log(response);
                $('#myModalCreateProduct').modal('hide');
            });
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
                    ids: JSON.stringify(product.getProductsIds())
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
            var stock_project = repo.stock_project > 0 ? repo.stock_project : 'Sin stock';

            return $(
                '<div class="wrapper container">' +
                '<div class="row">' +
                '<div class="col-lg-1">' +
                '<img alt="" src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                '</div>' +
                '<div class="col-lg-11 text-left shadow-sm">' +
                //'<br>' +
                '<p style="margin-bottom: 0;">' +
                '<b>Nombre:</b> ' + repo.full_name + '<br>' +
                '<b>Stock bodega: </b>' + stock + '<br>' +
                '<b>Stock poryecto: </b>' + stock_project +
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
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var delItem = sale.details.products.splice(tr.row, 1);
            sale.details.products_delete.push(delItem[0]);
            tblProducts.row(tr.row).remove().draw();
            sale.calculateInvoice();
        })
        .on('change', 'input', function (e) {
            console.clear();

            var value = $(this).val();
            var tr = tblProducts.cell($(this).closest('td, li')).index();

            // Costo del producto
            if (e.target.name === 'cost' || e.target.name === 'cant') {
                sale.details.products[tr.row][`${e.target.name}`] = parseFloat(value);
                sale.calculateInvoice();
                $('td:last', tblProducts.row(tr.row).node()).html(formatNumber(sale.details.products[tr.row].subtotal));
            }

            // Costo del Precio de venta
            if (e.target.name === 'pvp') {
                sale.details.products[tr.row].pvp = parseFloat(value);

            }

            // expiration
            if (e.target.name === 'expiration') {
                sale.details.products[tr.row].expiration = value;
            }
        })

    $('.btnRemoveAll').on('click', function () {
        if (sale.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            sale.details.products = [];
            product.listProducts();
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
                    'ids': JSON.stringify(product.getProductsIds()),
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
                {"data": "cost"},
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
                        var buttons = '<a rel="add" class="btn btn-success btn-xs"><i class="fas fa-plus"></i></a> ';
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
            product.addProduct(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    product.listProducts();


})