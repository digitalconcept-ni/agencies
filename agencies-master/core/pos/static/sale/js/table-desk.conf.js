var tableConf = {
    listProducts: function () {
        let action = $('input[name="action"]').val();
        sale.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: sale.products,
            columns: [
                {"data": "id"},
                {"data": "restore"},
                {"data": "full_name"},
                // {"data": "stock"},
                {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center',
                },
                {
                    targets: [0],
                    visible: false,
                },
                {
                    targets: [1],
                    render: function (data, type, row) {
                        var check = ` <div class="form-check form-switch">`
                        if (action === 'edit') {
                            if (row.before === true) {
                                if (data === false) {
                                    check += '<input class="form-check-input" type="checkbox"  rel="restore">'
                                } else {
                                    check += '<input class="form-check-input" type="checkbox"  rel="restore" checked>'
                                }
                            } else {
                                check += '<input class="form-check-input" type="checkbox" disabled>'
                            }
                        } else if (action === 'add') {
                            check += '<input class="form-check-input" type="checkbox"  rel="restore" disabled>'
                        }
                        check += `</div>`
                        return check;

                    }
                },
                {
                    targets: [2],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" style="color: blue; cursor: pointer">' + data + '</a>';
                    }
                },
                // {
                //     targets: [-4],
                //     orderable: false,
                //     render: function (data, type, row) {
                //         if (!row.is_inventoried) {
                //             return `<span class="badge bg-secondary">Sin stock</span>`
                //         }
                //         return `<span class="badge bg-secondary">${data}</span>`
                //     }
                // },
                {
                    targets: [-3],
                    orderable: false,
                    render: function (data, type, row) {
                        // var html = '<select name="selectPVP" id="selectPVP" class="form-control">';
                        // $.each(data, function (i, item) {
                        //     if (row.applied_price === i) {
                        //         html += `<option value="${item}" data-selection="${i}" selected>${i}: ${item}</option>`;
                        //     } else {
                        //         html += `<option value="${item}" data-selection="${i}">${i}: ${item}</option>`;
                        //     }
                        // })
                        // html += '</select>';
                        // return html;
                        // // return JSON.stringify(data);
                        return `${row.applied_price} | ${parseFloat(data).toFixed(2)}`;
                    }
                },
                {
                    targets: [-2],
                    orderable: false,
                    render: function (data, type, row) {
                        // if (row.restore === true) {
                        //     return '<input disabled type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cant + '">';
                        // } else {
                        //     return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cant + '">';
                        // }
                        return data;
                    }
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
            ],
        });
    },
}