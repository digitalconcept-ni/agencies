var select_client;

$(function () {
    select_client = $('select[name="client"]');


    // Client

    select_client.select2({
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
                    action: 'search_client'
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
    })
        .on('select2:select', function (e) {
            var data = e.params.data;

            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {'action': 'search_if_exits_client', 'id_client': data.id},
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            }).done(function (data) {
                if (data.exists) {
                    Swal.fire({
                        title: "Notificación",
                        text: "El cliente seleccionado ya cuenta con una venta",
                        icon: "warning",
                        confirmButtonColor: "#3085d6",
                        confirmButtonText: "Ok!"
                    }).then((result) => {
                        if (result.isConfirmed) {
                            location.href = data.success_url;
                        }
                    });
                }
                // else {
                //     var lat = e.params.data.lat;
                //     console.log(lat)
                //     if (lat != null || lat != undefined) {
                //         coordClient = true;
                //     } else {
                //         coordClient = false;
                //     }
                // }

            })
        });


    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function (e) {
        $('#frmClient').trigger('reset');
    });

    $('#frmClient').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente Cliente?', parameters, function (response) {
                //console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                select_client.append(newOption).trigger('change');
                $('#myModalClient').modal('hide');
            });
    });
})