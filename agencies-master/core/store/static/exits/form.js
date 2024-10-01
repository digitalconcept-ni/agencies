var select_client, select_search_product;

var list = {
    details: {
        status: '',
        products: [],
        products_delete: [],
    },
    getProductsIds: function () {
        return this.details.products.map(value => value.product_id);
    },
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
    },
    listProducts: function () {
        const action = $('input[name="action"]').val();

        tbExitsProducts = $('#tbListas').DataTable({
            // dom: 'Bftip',
            deferRender: true,
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            ordering: false,
            order: false,
            columns: [
                {"data": "product_id"},
                {"data": "product"},
                {"data": "cant"},
                {"data": "restore"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    visible: false,
                },
                {
                    targets: [0, 1, 2, 3],
                    class: 'text-center',
                },
                {
                    targets: [1],
                    render: function (data, type, row) {
                        if (row.category === 'INSUMOS' || row.category === 'MATERIA PRIMA') {
                            return `<a rel=remove style="color: #007bff; cursor: pointer">
                                <span class="btn btn-xs btn-success"> ${row.category}</span> - ${data}</a>`
                        } else {
                            return `<a rel=remove style="color: #007bff; cursor: pointer"> ${data} </a>`
                        }
                    },
                },
                {
                    targets: [2],
                    render: function (data, type, row) {
                        return `<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="${data}">`;
                    },
                },
                {
                    targets: [3],
                    class: 'text-center',
                    render: function (data, type, row) {

                        if (action === 'edit') {
                            if (row.category.toUpperCase() === 'INSUMOS' || row.category.toUpperCase() === 'MATERIA PRIMA') {
                                return '';
                            } else {
                                if (data === false) {
                                    return '<input type="checkbox" style="height: 15px;width: 15px;" rel="restore"/>';
                                } else {
                                    return '<input type="checkbox" style="height: 15px;width: 15px;" checked rel="restore" />';
                                }
                            }
                        } else if (action === 'add') {
                            if (row.category === 'INSUMOS' || row.category === 'MATERIA PRIMA') {
                                return '';
                            } else {
                                return '<input type="checkbox" style="height: 15px;width: 15px;" disabled/>';
                            }
                        }
                    },
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 10,
                    step: 1
                });

            },
        });
    },
};

var follow = {
    add: 0,
    del: 0,
}

$(function () {

    select_search_product = $('select[name="search_product"]');
    let action = $('input[name=action]').val();

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // ****************************
    // Boton de eliminar todos los items de la tabla
    $('.btnRemoveAll').on('click', function () {
        if (list.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            list.details.products = [];
            list.listProducts();
        }, function () {

        });
    });

    // BUSQUEDA DE PRODUCTOS

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
                    ids: JSON.stringify(list.getProductsIds())
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción o medidas',
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
            let insert = {};
            insert['product_id'] = data.id
            insert['product'] = data.text
            insert['category'] = data.category.name
            insert['cant'] = 1
            if (data.category.name.toUpperCase() === 'INSUMOS' || data.category.name.toUpperCase() === 'MATERIA PRIMA') {
                insert['restore'] = true
            } else {
                insert['restore'] = false
            }
            list.addProduct(insert);
            select_search_product.val('').trigger('change.select2');
        });

    // END BUSQUEDA DE PRODUCTOS

    //ELIMINACION DE UN EXPEDIENTE DE LA CAJA
    $('#tbListas tbody').on('click', 'a[rel="remove"]', function () {
        var tr = tbExitsProducts.cell($(this).closest('td, li')).index();
        var delItem = list.details.products.splice(tr.row, 1);
        list.details.products_delete.push(delItem[0]);
        tbExitsProducts.row(tr.row).remove().draw();
        list.listProducts();

    }).on('change', 'input[name="cant"]', function () {
        var cant = parseInt($(this).val());
        var tr = tbExitsProducts.cell($(this).closest('td, li')).index();
        if (action === 'edit') {
            if (!list.details.products[tr.row].hasOwnProperty('before_cant')) {
                list.details.products[tr.row]['before_cant'] = list.details.products[tr.row].cant;
            }
        }
        list.details.products[tr.row].cant = cant;
    }).on('click', 'input[rel="restore"]', function () {
        // DETALLE DEL ESTATUS DEL CONTRATO
        let tr = tbExitsProducts.cell($(this).closest('td, li')).index();
        let data = tbExitsProducts.row(tr.row).index();
        const _this = $(this);

        if (_this.prop('checked')) {
            list.details.products[data].restore = true
        } else {
            list.details.products[data].restore = false
        }
    })

    // EXIT ESTATUS
    function BoxStatus() {
        let R = 0; // REVISADO
        let NR = 0; // NO REVISADO
        let status;

        $.each(list.items.credit, function (k, v) {
            if (v.exists === 0 || v.exists === '0') {
                NR += 1;
            } else if (v.exists === 1 || v.exists === '1') {
                R += 1;
            }
        });

        if (NR > 0 && R === 0) {
            status = 0
        } else if (R > 0 && NR === 0) {
            status = 2;
        } else if (R > 0 && NR > 0) {
            status = 1;
        }
        return status;
    }

    // funcion para recolectar datos de la caja
    function box_detail() {
        $.each(list.items, function (v) {
            if (v === 'credit' || v === 'follow') {
                return true;
            } else if (v === 'status') {
                list.items[v] = BoxStatus();
            } else {
                list.items[v] = $('#id_' + v + '').val();
            }
        });
    }

    //Event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        if (list.details.products.length === 0) {
            message_error({'Error de guardado': 'Agregue resgistros al detalle'});
            return false;
        } else {
            // box_detail();
            //var parameters = $(this).serializeArray();
            var success_url = this.getAttribute('data-url');

            var parameters = new FormData(this);
            if (action == 'edit') {
                parameters.append('products_delete', JSON.stringify(list.details.products_delete));
            }
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('products', JSON.stringify(list.details.products));
            // parameters.append('follow', JSON.stringify(follow));

            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                location.href = success_url;
            });

        }
    });
    list.listProducts();
});