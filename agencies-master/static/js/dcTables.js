/*
Libreria auxiliar para data tables
Designed by Bryan Urbina Guevara | Digital Concept

se esta utilizando asyncronia para no tener errores en el procesodel dibujado

url = URL a donde haremos la llamada mediante AJAX
action = La accion en la vista donde recolectara la informacion para dibujar (metodo post)
insertInto = Indica en que tabla de todo el lienzo vamos a dibujar la tabla
th = Define una celda de encabezado en una tabla
table = nombre de la tabla donde se dibujara
modal = true (Mostrar el modal en caso que hayan datos que mostrar en tabla del modal) ---  false (para no mostrar el modal
config = configuracion por separado de las columnas formato de DataTables ejm:
config = [{
             targets: [0, 1],
             class: 'text-center'
          }];
  modal: true / false (si la tabla esta dentro de un modal esta opcion activa el modal)
*/

const clean = (table, insertInto) => {

    return new Promise((resolve) => {
        let tr = $(`tr[rel='${insertInto}']`); // fila de la tabla donde se insertaran los encabezados

        if (!$.trim(tr.html()).length) {
            resolve(true)
        } else {
            try {
                // Si tiene contenido lo limpia y devuelve true para proceder con el proceso
                let tableName = $(`#${table}`);
                tr.empty();
                tableName.DataTable().clear();
                tableName.DataTable().destroy();
                resolve(true);
            } catch (error) {
                console.log(error)
            }
        }
    })
}

const tableColumn = async (data, table, insertInto) => {
    const cleaned = await clean(table, insertInto);

    if (cleaned === true) {
        let trow = $(`#${table} tr[rel=${insertInto}]`).empty();
        let th = '';
        $.each(data, v => {
            th += `<th style="width: auto">${data[v]}</th>`;
        })
        trow.append(th)
    }
    return true;
}

const drawTables = async (data) => {
    var header = await tableColumn(data.th, data.table, data.inserInto);

    if (header === true) {
        $.fn.dataTable.ext.errMode = 'none';

        tableData = $(`#${data.table}`).on('error.dt', function (e, settings, techNote, message) {
            message_error(message.split('-')[1]);
        }).DataTable({
            // dom: 'Btip',
            // buttons: {
            //     dom: {
            //         button: {
            //             className: 'btn'
            //         }
            //     },
            //     buttons: [
            //         {
            //             extend: "excel",
            //             text: 'Exportar a Excel',
            //             className: 'btn btn-outline-success'
            //         }
            //     ]
            // },
            deferRender: true,
            responsive: true,
            autoWidth: false,
            destroy: true,
            orderable: false,
            ajax: {
                url: data.url,
                type: 'POST',
                // data: data.data,
                data: {
                    'action': data.action,
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columnDefs: data.config,
            initComplete: function (settings, json) {
                if (!json.hasOwnProperty('error')) {
                    if (data.modal === true) {
                        $('#modalInfo').modal('show');
                    }
                }
            }
        })
    }
}