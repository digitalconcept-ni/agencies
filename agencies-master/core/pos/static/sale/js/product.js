var tblProducts;
var select_search_product;

$(function () {
    var action = $('input[name="action"]').val();

    select_search_product = $('select[name="search_product"]');

    // Funcion para mostrar el detalle en modal el producto antes de insertarlo

    const showProduct = (data) => {
        var html = '<div class="row">';
        html += '<div class="col-6">';
        html += `<input name="inputCant" value="${data.cant}" id="inputCant" class="form-control" placeholder="Ingresa la cantidad">`;
        html += '</div>'
        html += '<div class="col-6">';
        html += '<select name="selectPVP" id="selectPVP" class="form-control">';

        $.each(data.pvp_list, function (i, item) {
            if (data.applied_price === i) {
                html += `<option value="${item}" data-selection="${i}" selected>${i}: ${item}</option>`;
            } else {
                html += `<option value="${item}" data-selection="${i}">${i}: ${item}</option>`;
            }
        })
        html += '</select>';
        html += '</div>';
        html += '</div>';

        Swal.fire({
            title: data.full_name,
            // allowOutsideClick: false,
            showCancelButton: false,
            showDenyButton: true,
            confirmButtonColor: "#198754",
            denyButtonColor: "#d33",
            confirmButtonText: '<i class="bi bi-floppy"></i>',
            denyButtonText: '<i class="bi bi-trash3"></i>',
            // cancelButtonText: "Eliminar",
            html: html,
            focusConfirm: false,
            preConfirm: () => {
                const cant = Swal.getPopup().querySelector('#inputCant').value;
                const select = Swal.getPopup().querySelector('#selectPVP');
                const selectedOption = select.options[select.selectedIndex]; // Obtenemos la <option> seleccionada

                const selectValue = selectedOption.value; // El valor normal del option
                const dataAppliedPrice = selectedOption.dataset.selection; // Accedemos al atributo data-categoria

                if (!cant || !select) {
                    Swal.showValidationMessage(`Por favor, ingresa una cantidad valida.`);
                    return false; // Evita que el SweetAlert se cierre
                }
                return {cant: cant, select: selectValue, applied_price: dataAppliedPrice};
            }
        }).then((result) => {
            if (result.isConfirmed) {
                const {cant, select, applied_price} = result.value;
                if (!data.hasOwnProperty('index')) {
                    data.cant = cant;
                    data.pvp = select;
                    data.applied_price = applied_price;
                    sale.addProduct(data);
                } else {
                    sale.products[data.index].cant = cant;
                    data.pvp = select;
                    data.applied_price = applied_price;
                }

                tableConf.listProducts();
            }
            if (result.isDenied) {
                let delItem = sale.products.splice(data.index, 1);
                delItem[0].delete = true;
                sale.products_delete.push(delItem[0]);
                tableConf.listProducts();
            }
        });
    }


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
            var stock = '';
            if (repo.control_stock) {
                stock += `<b>Stock:</b> ${repo.is_inventoried ? repo.stock : 'Sin stock'} <br>`;
            }

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
                stock +
                // '<b>Stock:</b> ' + stock + '<br>' +
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
            // data.applied_price = 'pvp';
            data.cant = 1;
            data.subtotal = 0.00;
            // data.pvp = data.pvp_list.pvp; //al momento de insertar se carga el precio de publico general
            showProduct(data)
            // sale.addProduct(data);
            // tableConf.listProducts();
            select_search_product.val('').trigger('change.select2');
        });

    $('#tblProducts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function (e) {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            data = sale.products[tr.row]
            data.index = tr.row; // Agregamos un index al array para saber que posicion vamos a tratar
            showProduct(data)
            // alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
            //     function () {
            //         let delItem = sale.products.splice(tr.row, 1);
            //         delItem[0].delete = true;
            //         sale.products_delete.push(delItem[0]);
            //         tableConf.listProducts();
            //     });
        })
        .on('change', 'select[name="selectPVP"]', function (e) {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            let _this = $(this);
            const selectedOption = _this.find('option:selected');

            sale.products[tr.row]['applied_price'] = selectedOption.data().selection;
            sale.products[tr.row]['pvp'] = selectedOption.val();
            // console.clear();
            // var cant = parseInt($(this).val());
            // if (action === 'edit') {
            //     if (sale.products[tr.row].hasOwnProperty('before') &&
            //         !sale.products[tr.row].hasOwnProperty('initial_amount')) {
            //     }
            // }
            //
            // sale.products[tr.row].cant = cant;
            sale.calculateInvoice();
            $('td:last', tblProducts.row(tr.row).node()).html(sale.products[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="cant"]', function (e) {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            if (action === 'edit') {
                if (sale.products[tr.row].hasOwnProperty('before') &&
                    !sale.products[tr.row].hasOwnProperty('initial_amount')) {
                    sale.products[tr.row]['initial_amount'] = sale.products[tr.row][e.target.name];
                }
            }

            sale.products[tr.row].cant = cant;
            sale.calculateInvoice();
            $('td:last', tblProducts.row(tr.row).node()).html(sale.products[tr.row].subtotal.toFixed(2));
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
                let s = parseFloat(sale.details.products[tr.row].cant) * parseFloat(sale.details.products[tr.row].pvp);
                $('td:last', tblProducts.row(tr.row).node()).html(s.toFixed(2));

                // Deshabilitar el input
                cantInput.prop('disabled', false);

            }
            sale.calculateInvoice();
        })

    $('.btnRemoveAll').on('click', function () {
        if (sale.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            sale.products = [];
            tableConf.listProducts();
        }, function () {

        });
    });

    tableConf.listProducts();
})