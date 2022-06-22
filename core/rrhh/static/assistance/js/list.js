var input_year;
var select_month;

function load() {
    table = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                action: 'load',
                year: $('#year').val(),
                month: $('#month').val(),
            },
            dataSrc: ""
        },
        columns: [
            {data: "id"},
            {data: "year"},
            {data: "month"},
            {data: "day"},
            {data: "present"},
            {data: "faults"},
            {data: "assistances"},
        ],
        columnDefs: [
            {
                targets: [-1],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<a href="/rrhh/assistance/update/' + row.id + '/" data-toggle="tooltip" title="Editar registro" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit" aria-hidden="true"></i></a> ';
                    buttons += '<a href="/rrhh/assistance/delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash" aria-hidden="true"></i></a> ';
                    buttons += '<a rel="details" data-toggle="tooltip" title="Ver asistencia" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search" aria-hidden="true"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<span class="badge badge-success">' + data + '</span>';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<span class="badge badge-danger">' + data + '</span>';
                }
            }
        ],
    });
}

$(function () {

    select_month = $('select[name="month"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    input_year = $('input[name="year"]');

    input_year.datetimepicker({
        locale: 'es',
        keepOpen: false,
        viewMode: 'years',
        format: 'YYYY'
    });

    input_year.datetimepicker('date', new moment().format('YYYY'));

    input_year.on('change.datetimepicker', function (e) {
        load();
    });

    load();

    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var td = table.cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data();
        $('#tblAssistance').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: rows.assistances,
            columns: [
                {data: "id"},
                {data: "cont.emp.user.full_name"},
                {data: "state"},
                {data: "id"},
                {data: "desc"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<b class="badge badge-success">Si</b>';
                        }
                        return '<b class="badge badge-danger">No</b>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if(row.event !== null){
                            return row.event.type;
                        }
                        return '---';
                    }
                },
            ]
        });
        $('#myModalAssistance').modal('show');
    });

    select_month.on('change', function () {
        load();
    });

    select_month.val('').trigger('change');

});
