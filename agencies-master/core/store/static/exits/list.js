var select_technician, select_search_product;

// Funcion para mostrar datos de la tabla branches
var exits = {
    details: {
        cards: []
    },
    config: [
        {
            targets: [0, 1, 2, 3, 4, 5, 6],
            class: 'text-center',
        },
        {
            targets: [3],
            class: 'text-center',
            render: function (data, type, row) {
                if (data === false) {
                    let card = '<a class="btn btn-xs btn-danger">PENDIENTE</a>'
                    return card;
                } else if (data === true) {
                    let card = '<a class="btn btn-xs btn-success">COMPLETA</a>'
                    return card;
                }
            },
        },
        {
            targets: [6],
            class: 'text-center',
            //orderable: false,
            render: function (data, type, row) {
                var buttons = '<a title="Detalle de salida" rel="detExit" class="btn btn-success btn-xs btn-flat" style="color: white; background: #009900;"><i class="fas fa-info-circle"></i></a>';
                buttons += '<a title="Editar registro" href="' + pathname + 'update/' + row[0] + '/" style="margin: 0 5px 0 5px;" class="btn btn-xs btn-flat btn-warning superUserEdit"><i class="fas fa-edit"></i></a>';
                buttons += '<a title="Eliminar registro"  rel="delete" class="btn btn-danger btn-xs btn-flat" style="color: white"><i class="fas fa-trash"></i></a>';
                // buttons += '<a title="Historial de modificaciones" rel="history" type="button" class="btn" style="color: white !important; background: #008f39; margin-left: 5px"><i class="bi bi-clock-history"></i></a>';
                // if (row[7][0] === true) {
                // } else {
                //     if (row[7][1] === true) {
                //         return buttons;
                //     } else {
                //         if (row[4] === 2 || row[4] === '2') {
                //             return buttons;
                //         } else {
                //             buttons += '<a title="Editar registro" href="/sucursales/exits/edit/' + row[0] + '/" type="button" style="margin: 0 5px 0 5px;" class="btn btn-secondary superUserEdit"><i class="bi bi-pencil-square"></i></a>';
                //         }
                //     }
                // }
                return buttons;
            },
        }],
    list: function (info) {
        var action;
        if (info.action === 'search_product_detail') {
            action = {
                'action': info.action,
                'id': info.id
            };
        } else if (info.action === 'search_technician_detail') {
            action = {
                'action': info.action,
                'id': info.id
            };
        } else if (info.action === 'all') {
            action = {'action': 'search_data'};
        }

        let data = {
            'data': action,
            'inserInto': 'rowList',
            'th': ['Nro salida', 'Cliente', 'Técnico', 'Estatus', 'Creado por', 'Fecha', 'Opciones'],
            'table': 'tableList',
            'config': this.config,
            'modal': false,
        }
        drawTables(data);

        $.each(this.details.cards, function (k, v) {
            $(`#${k}`).text(v)
        })
    },

};

$(function () {
    // Inicializador de las vistas de la informacion
    exits.list({action: 'all'});

    select_search_product = $('select[name="search_product"]');
    select_technician = $('select[name="select_technician"]');

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
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
                    // ids: JSON.stringify(list.getProductsIds())
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
                '<b>Categoria:</b> <span class="badge badge-success">' + repo.category.name + '</span>' + '<br>' +
                '<b>Codigo:</b> <span class="badge badge-dark">' + repo.code + '</span>' +
                '</p>' +
                '</div>' +
                '</div>' +
                '</div>');
        },
    })
        .on('select2:select', function (e) {
            var data = e.params.data;
            let info = {
                action: 'search_product_detail',
                id: data.id
            }
            exits.list(info);
            select_search_product.val('').trigger('change.select2');
        });

    // END BUSQUEDA DE PRODUCTOS

    // BUSQUEDA DE TECNICOS

    select_technician.select2({
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
                    action: 'search_technician_select2',
                    // ids: JSON.stringify(list.getProductsIds())
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese nombre o roll',
        minimumInputLength: 1,
        templateResult: function (repo) {
            if (repo.loading) {
                return repo.text;
            }

            if (!Number.isInteger(repo.id)) {
                return repo.text;
            }
            return $(
                '<div class="wrapper container">' +
                '<div class="row">' +
                // '<div class="col-lg-1">' +
                // '<img alt="" src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                // '</div>' +
                '<div class="col-lg-11 text-left shadow-sm">' +
                //'<br>' +
                '<p style="margin: 10px 0px;">' +
                '<b>Nombre:</b> ' + repo.name + '<br>' +
                '<b>Roll:</b> <span class="badge badge-danger">' + repo.position + '</span>' +
                '</p>' +
                '</div>' +
                '</div>' +
                '</div>');
        },
    })
        .on('select2:select', function (e) {
            var data = e.params.data;
            let info = {
                action: 'search_technician_detail',
                id: data.id
            }
            exits.list(info);
            select_technician.val('').trigger('change.select2');
        });

    // END BUSQUEDA DE TECNICOS


    $('#tableList tbody')
        .off()
        .on('click', 'a[rel="detExit"]', function (e) {
            var table = $('#tableList').DataTable();
            var tr = table.cell($(this).closest('td, li')).index();
            var data = table.row(tr.row).data();

            let config = [
                {
                    targets: [0, 1, 2],
                    class: 'text-center',
                    //orderable: false,
                },
                {
                    targets: [0],
                    render: function (data, type, row) {
                        if (row.category === 'INSUMOS' || row.category === 'MATERIA PRIMA') {
                            return `<a style="color: #001f3f; cursor: pointer">
                                <span class="btn btn-xs btn-success"> ${row.category}</span> - ${data}</a>`
                        } else {
                            return `<a style="color: #001f3f; cursor: pointer"> ${data} </a>`
                        }
                    }
                },
                {
                    targets: [2],
                    render: function (data, type, row) {
                        if (row.category.toUpperCase() === 'INSUMOS' || row.category.toUpperCase() === 'MATERIA PRIMA') {
                            return '';
                        } else {
                            if (data === false) {
                                return '<input type="checkbox" disabled/>';
                            } else if (data === true) {
                                return '<input type="checkbox" checked disabled/>';
                            }
                        }
                    },
                },
            ];

            $('#tblExits').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_exit_detail',
                        'id': data[0]
                    },
                    dataSrc: "",
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                },
                columns: [
                    {"data": "product"},
                    {"data": "cant"},
                    {"data": "restore"},
                ],
                columnDefs: config,
            });
            $('#modalExit').modal('show');

        }).on('click', 'a[rel="history"]', function () {
        var table = $('#tableList').DataTable();
        var tr = table.cell($(this).closest('td, li')).index();
        var data = table.row(tr.row).data();

        let config = [
            {
                targets: [0],
                visible: false,
            },
            {
                targets: [1, 2, 3, 4, 5, 6, 7],
                class: 'text-center',
            },
        ]

        let dataModal = {
            'action': {
                'action': 'search_history',
                'id': data[0]
            },
            'inserInto': 'rowListModal',
            'th': ['id', 'Nro. Caja', 'Usuario', 'Fecha', 'Comentario'],
            'table': 'tableListModal',
            'config': config,
            'modal': true,
        }
        drawTables(dataModal);

    })

})