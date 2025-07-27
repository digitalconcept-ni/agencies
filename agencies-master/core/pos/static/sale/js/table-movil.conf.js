var tableConf = {
    listProducts: function () {
        sale.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: false,
            autoWidth: true,
            destroy: true,
            paging: false,
            dom: 't',
            // scrollY: '58vh',
            // scrollCollapse: true,
            data: sale.products,
            columns: [
                {"data": "id"},
                {"data": "full_name"},
                {"data": "cant"},
                {"data": "pvp"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                 {
                    targets: '_all',
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [0],
                    visible: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [1],
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn-xs" style="font-size: 12px; font-weight: bold">' + data + '</a>';
                    }
                },
                {
                    targets: [2],
                    render: function (data, type, row) {
                        return data
                        // return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [3],
                    render: function (data, type, row) {
                        return `${row.applied_price} ${parseFloat(data).toFixed(2)}`;
                    }
                },{
                    targets: [4],
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
            ],
        });
    },
}