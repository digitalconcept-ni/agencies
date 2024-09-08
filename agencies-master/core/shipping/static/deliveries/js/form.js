$(function () {

    // select_client = $('select[name="client"]');
    //
    // $('.select2').select2({
    //     theme: "bootstrap4",
    //     language: 'es'
    // });
    //
    // select_search_product.select2({
    //     theme: "bootstrap4",
    //     language: 'es',
    //     allowClear: true,
    //     ajax: {
    //         delay: 250,
    //         type: 'POST',
    //         url: pathname,
    //         headers: {
    //             'X-CSRFToken': csrftoken
    //         },
    //         data: function (params) {
    //             return {
    //                 term: params.term,
    //                 action: 'search_products_select2',
    //                 ids: JSON.stringify(loss.getProductsIds())
    //             };
    //         },
    //         processResults: function (data) {
    //             return {
    //                 results: data
    //             };
    //         },
    //     },
    //     placeholder: 'Ingrese una descripción',
    //     minimumInputLength: 1,
    //     templateResult: function (repo) {
    //         if (repo.loading) {
    //             return repo.text;
    //         }
    //
    //         if (!Number.isInteger(repo.id)) {
    //             return repo.text;
    //         }
    //
    //         var stock = repo.is_inventoried ? repo.stock : 'Sin stock';
    //
    //         var tax = '';
    //
    //         if (repo.tax === 'e' || repo.tax === 'exento') {
    //             tax = 'Exento';
    //         } else if (repo.tax === 'g' || repo.tax === 'grabado') {
    //             tax = 'Grabado'
    //         }
    //         return $(
    //             '<div class="wrapper container">' +
    //             '<div class="row">' +
    //             // '<div class="col-lg-1">' +
    //             // '<img alt="" src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
    //             // '</div>' +
    //             '<div class="col-lg-11 text-left shadow-sm">' +
    //             //'<br>' +
    //             '<p style="margin-bottom: 0;">' +
    //             '<b>Nombre:</b> ' + repo.full_name + '<br>' +
    //             '<b>Stock:</b> ' + stock + '<br>' +
    //             '<b>PVP:</b> <span class="badge badge-warning">$' + repo.pvp + '</span>' + '<br>' +
    //             '<b>Tipo:</b> <span class="badge badge-dark">' + tax + '</span>' +
    //             '</p>' +
    //             '</div>' +
    //             '</div>' +
    //             '</div>');
    //     },
    // })
    //     .on('select2:select', function (e) {
    //         var data = e.params.data;
    //         if (!Number.isInteger(data.id)) {
    //             return false;
    //         }
    //         data.cant = 1;
    //         data.subtotal = 0.00;
    //         loss.addProduct(data);
    //         select_search_product.val('').trigger('change.select2');
    //     });

    $('#shipping_date').datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    $('#delivery_date').datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });
});

