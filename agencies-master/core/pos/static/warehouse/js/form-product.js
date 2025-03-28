var tblProducts;
var select_search_product, tblSearchProducts, select_category;

var product = {
    categoryID: [],
    getCategoryIds: function () {
        return this.categoryID.map(value => value.id);
    },
    getProductsIds: function () {
        return warehouse.details.products.map(value => value.id);
    },
    addProduct: function (item) {
        warehouse.details.products.push(item);
        // this.listProducts();
    },
    listProducts: function () {

        // warehouse.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: warehouse.details.products,
            columns: [
                {"data": "id"},
                {"data": "full_name"},
                {"data": "cant"},
            ],
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center',
                },
                {
                    targets: [0],
                    render: function (data, type, row) {
                        return `<a rel="remove" class="btn btn-danger btn-sm"><i class="bi bi-trash3"></i></a>`;
                    }
                },
                {
                    targets: [2],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="number" min="1" max="10000" step="0.01" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },

            ],
        });
    },
};

$(function () {
    var action = $('input[name="action"]').val();

    select_search_product = $('select[name="search_product"]');
    select_category = $('select[name="category"]');


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
        placeholder: 'Ingrese nombre o codigo',
        minimumInputLength: 1,
        templateResult: function (repo) {
            if (repo.loading) {
                return repo.text;
            }

            if (!Number.isInteger(repo.id)) {
                return repo.text;
            }

            var stock = repo.is_inventoried ? repo.stock : 'Sin stock';

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
                '<b>Stock: </b>' + stock + '<br>' +
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
            product.addProduct(data);
            product.listProducts();
            select_search_product.val('').trigger('change.select2');
        });

    $('#tblProducts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var delItem = warehouse.details.products.splice(tr.row, 1);
            warehouse.details.products_delete.push(delItem[0]);
            tblProducts.row(tr.row).remove().draw();
            warehouse.calculateInvoice();
        })
        .on('change', 'input', function (e) {
            console.clear();

            var value = $(this).val();
            var tr = tblProducts.cell($(this).closest('td, li')).index();

            // Costo del producto
            if (e.target.name === 'cant') {
                warehouse.details.products[tr.row][`${e.target.name}`] = parseFloat(value);
                // warehouse.calculateInvoice();
                // $('td:last', tblProducts.row(tr.row).node()).html(formatNumber(warehouse.details.products[tr.row].subtotal));
            }
        })

    $('.btnRemoveAll').on('click', function () {
        if (warehouse.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            warehouse.details.products = [];
            product.listProducts();
        }, function () {

        });
    });

    select_category.select2().on('select2:select', function (e) {
        // Agregamos el preloader al body
        document.body.prepend(preloader);
        let categoryId = $(this).val();
        // Desabilitamos el option seleccionad para no volver a cargar los datos
        let selectElement = $(e.params.data.element);
        selectElement.prop('disabled', true);

        var parameters = new FormData();

        parameters.append('categoryID', categoryId);
        parameters.append('action', 'get_product_by_category');

        $.ajax({
            url: pathname,
            data: parameters,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
            success: function (request) {

                console.log(request);

                request.forEach(item => {
                    item.cant = item.stock;
                    product.addProduct(item);
                })
                product.listProducts();

                // Quitamos el preloader cuando se haya cumplido la accion
                if (preloader) {
                    preloader.remove();
                }

            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        })
    });

    product.listProducts();


})