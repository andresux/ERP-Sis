var tblResult;
var input_datejoined;

function search() {
    tblResult = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'search',
                'date_joined': $('#date_joined').val(),
                'product': $('#product').val(),
            },
            dataSrc: ""
        },
        columns: [
            {data: "id"},
            {data: "ing.nro"},
            {data: "ing.date_joined"},
            {data: "prod.name"},
            {data: "prod.cat.name"},
            {data: "cant"},
            {data: "saldo"},
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4],
                class: 'text-center',
            },
            {
                targets: [5],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<span class="badge label label-success">' + data + '</span>'
                }
            },
            {
                targets: [6],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<span class="badge label label-danger">' + data + '</span>'
                }
            },
        ],
    });
}

$(function () {

    input_datejoined = $('input[name="date_joined"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    }).on('change', function () {
        search();
    });

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    input_datejoined.on('change.datetimepicker', function (e) {
        search();
    });

    search();
});