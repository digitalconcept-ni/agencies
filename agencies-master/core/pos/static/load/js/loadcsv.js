$(function () {

    $('#btn_insert_csv').on('click', function () {

        if ($('#insert_file').val() === '') {
            message_error({'error': 'Selecciones un documento para poder insertarlo'})
        } else {
            let loader = document.querySelector('.preloader-container');

            const data = new FormData();
            data.append('file', $('#insert_file')[0].files[0]);
            data.append('action', 'insert_file');

            $.ajax('.', {
                method: "POST",
                data: data,
                contentType: false,
                processData: false,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (response) {
                    loader.style.opacity = 0
                    loader.style.visibility = 'hidden'
                    if (response.hasOwnProperty('error')) {
                        message_error(response.error)
                    } else {
                        message_info(response.success)
                    }
                }
            })
        }
    })
})