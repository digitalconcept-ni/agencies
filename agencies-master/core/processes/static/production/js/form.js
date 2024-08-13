var tblProducts;
var select_client, select_search_product;
var tblSearchProducts;

var production = {
    details: {
        products: [],
        products_review: []
    },
    getProductsIds: function () {
        return this.details.products.map(value => value.id);
    },
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
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
            initComplete: function (settings, json) {

            }
        });
    },
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
            console.log(data)
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
        // .on('change', 'input[name="cant"]', function () {
        //     console.clear();
        //     console.log(production.details.products);
        //     var cant = parseInt($(this).val());
        //     var tr = tblProducts.cell($(this).closest('td, li')).index();
        //     production.details.products[tr.row].cant = cant;
        // });

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

    $('input[name="date_process"]').datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });
    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    $('#frmproduction').on('submit', function (e) {
        e.preventDefault();

        if (production.details.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('products', JSON.stringify(production.details.products));
        parameters.append('products_review', JSON.stringify(production.details.products_review));
        submit_with_ajax(pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = success_url;
        });
    });

    production.listProducts();
});

