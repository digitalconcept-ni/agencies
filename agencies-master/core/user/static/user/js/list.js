var user = {
    config: [
        {
            targets: '_all',
            orderable: false,
            class: 'text-center',
        },
        {
            targets: [0],
            render: function (data, type, row) {
                if (row[10] === true) {
                    return '<span class="badge bg-success">Pre venta</span>';
                }
            }
        },
        {
            targets: [5],
            render: function (data, type, row) {
                return '<img alt="" src="' + data + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
            }
        },
        {
            targets: [6],
            render: function (data, type, row) {
                if (data === true) {
                    return `<span class="badge bg-success"><i class="bi bi-check-circle"></i></span>`;
                } else {
                    return `<span class="badge bg-danger"><i class="bi bi-ban"></i></span>`;
                }
            }
        },
        {
            targets: [8],
            render: function (data, type, row) {
                if (data === true) {
                    return '<span class="badge bg-success p-2 rounded"> </span>';
                } else {
                    return '<span class="badge bg-danger p-2 rounded"> </span>';
                }
            }
        },
        {
            targets: [9],
            render: function (data, type, row) {
                var html = '';
                $.each(data, function (key, value) {
                    html += `<span class="badge bg-success">${value.name}</span>`;
                });
                return html;
            }
        },
        {
            targets: [-1],
            render: function (data, type, row) {
                return `<a href="${pathname}update/${row[0]}/" class="btn btn-warning btn-sm"><i class="bi bi-pencil-square"></i></a>`;
                // buttons += '<a rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                // return buttons;
            }
        },
    ],
    list: function () {

        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['', 'Nombres', 'Nombre de usuario', 'Telefono','Registro', 'Imagen', '¿Es Super Usuario?', 'Ultimo ingreso', 'Estado', 'Grupos', 'Opciones'],
            'table': 'tableList',
            'config': user.config,
            'modal': false,
        }

        drawTables(data);

        // $('#data').DataTable({
        //     responsive: true,
        //     autoWidth: false,
        //     destroy: true,
        //     deferRender: true,
        //     ajax: {
        //         url: pathname,
        //         type: 'POST',
        //         data: {
        //             'action': 'search'
        //         },
        //         dataSrc: "",
        //         headers: {
        //             'X-CSRFToken': csrftoken
        //         },
        //     },
        //     columns: [
        //         {"data": "id"},
        //         {"data": "full_name"},
        //         {"data": "username"},
        //         {"data": "date_joined"},
        //         {"data": "image"},
        //         {"data": "is_superuser"},
        //         {"data": "is_active"},
        //         {"data": "groups"},
        //         {"data": "id"},
        //     ],
        //     columnDefs: [
        //         {
        //             targets: [0],
        //             class: 'text-center',
        //             orderable: false,
        //             render: function (data, type, row) {
        //                 if (row.presale === true) {
        //                     return '<span class="badge badge-success badge-pill">' + 'Pre venta' + '</span>';
        //                 } else {
        //                     return ' ';
        //                 }
        //             }
        //         },
        //         {
        //             targets: [4],
        //             class: 'text-center',
        //             orderable: false,
        //             render: function (data, type, row) {
        //                 return '<img alt="" src="' + row.image + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
        //             }
        //         },
        //         {
        //             targets: [5],
        //             class: 'text-center',
        //             orderable: false,
        //             render: function (data, type, row) {
        //                 if (data === true) {
        //                     return '<span class="badge badge-success badge-pill">' + 'Si' + '</span>';
        //                 } else {
        //                     return '<span class="badge badge-danger badge-pill">' + 'No' + '</span>';
        //                 }
        //             }
        //         },
        //         {
        //             targets: [6],
        //             class: 'text-center',
        //             orderable: false,
        //             render: function (data, type, row) {
        //                 if (data === true) {
        //                     return '<span class="badge badge-success badge-pill">' + 'Activo' + '</span>';
        //                 } else {
        //                     return '<span class="badge badge-danger badge-pill">' + 'Bloqueado' + '</span>';
        //                 }
        //             }
        //         },
        //         {
        //             targets: [-2],
        //             class: 'text-center',
        //             orderable: false,
        //             render: function (data, type, row) {
        //                 var html = '';
        //                 $.each(row.groups, function (key, value) {
        //                     html += '<span class="badge badge-success">' + value.name + '</span> ';
        //                 });
        //                 return html;
        //             }
        //         },
        //         {
        //             targets: [-1],
        //             class: 'text-center',
        //             orderable: false,
        //             render: function (data, type, row) {
        //                 var buttons = '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
        //                 buttons += '<a rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
        //                 return buttons;
        //             }
        //         },
        //     ],
        //     initComplete: function (settings, json) {
        //
        //     }
        // });
    }
};

$(function () {
    user.list();
});