var info = {
    list: function (all) {
        var parameters = {
            'action': 'search_lower_inventory',
        };

        tblInfo = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: parameters,
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "category.name"},
                {"data": "image"},
                {"data": "is_inventoried"},
                {"data": "stock"},
                {"data": "pvp"},
            ],
            columnDefs: [
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img alt="" src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.is_inventoried) {
                            return '<span class="badge badge-success">Si</span>';
                        }
                        return '<span class="badge badge-warning">No</span>';
                    }
                },
                {
                    targets: [5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.is_inventoried) {
                            return '<span class="badge badge-secondary">Sin stock</span>';
                        }
                        if (row.stock > 6) {
                            return '<span class="badge badge-success">' + data + '</span>';
                        }
                        return '<span class="badge badge-danger">' + data + '</span>';
                    }
                },
                {
                    targets: [6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#myModalLowerInvetory').modal('show');
    },
    callInfo: function () {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'search_cards_data'},
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
        }).done(function (data) {
            $.each(data, v => {
                $(`#${v}`).text(data[v])
            });
        })
    }
};

$(function () {
    info.callInfo()
    setInterval(function () {
        info.callInfo()
    }, 15000)

    $('#btn-lower-inventory').on('click', function () {
        info.list()
    })

    $('#btn-sale-products').on('click', function () {
        $('#myModalLowerInvetory').modal('hide');

    })

})