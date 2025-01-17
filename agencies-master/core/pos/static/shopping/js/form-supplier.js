$(function () {

    let select_supplier = $('select[name="supplier"]');

    select_supplier.select2({
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
                    action: 'search_supplier'
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
    });

    // Event to open the model for create a new supplier
    $('.btnAddSupplier').on('click', function () {
        $('#myModalSupplier').modal('show');
    });


    $('#myModalSupplier').on('hidden.bs.modal', function (e) {
        $('#frmSupplier').trigger('reset');
    });


    // Form to create a new Supplier
    $('#frmSupplier').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_supplier');
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente proveedor?', parameters, function (response) {
                //console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                select_supplier.append(newOption).trigger('change');
                $('#myModalSupplier').modal('hide');

            });
    });
})
