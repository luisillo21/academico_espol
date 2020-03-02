/*function format(d) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Aula:</td>' +
        '<td>' + d.aula + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Facilitador(docente):</td>' +
        '<td>' + d.docente + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Aliado:</td>' +
        '<td>' + d.aliado + '</td>' +
        '</tr>' +
        '</table>';
}*/

$(document).ready(function () {
    var table = $('#tabla_evento').DataTable({
        "ajax": "/static/data/eventos.json",
        "columns": [
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            { "data": "codigo" },
            { "data": "nombre" },
            { "data": "tipo" },
            { "data": "modalidad" },
            /*{
                "className": 'center',
                "orderable": false,
                "data": null,
                "defaultContent": '<a href="#" class="editor_edit">Edit</a> / <a href="#" class="editor_remove">Delete</a>'
            }*/

        ]
    });
    console.log(document.getElementById("tabla_evento").lastChild);
    

    $('#tabla_evento tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });

    
});

