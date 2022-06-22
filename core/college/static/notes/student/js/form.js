var select_course;
var tblNotes;

$(function () {
    select_course = $('select[name="course"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_course.on('change', function () {
        tblNotes = $('#tblNotes').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_notes',
                    'id': select_course.val()
                },
                dataSrc: ""
            },
            columns: [
                {data: "name"},
                {data: "name"},
                {data: "id"},
                {data: "id"},
                {data: "id"},
                {data: "id"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(row.qualif[0].calif).toFixed(2);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(row.qualif[1].calif).toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(row.qualif[2].calif).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var calif = 0.00;
                        $.each(row.qualif, function (i, item) {
                            calif += parseFloat(item.calif);
                        });
                        return (calif / row.qualif.length).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var calif = 0.00;
                        $.each(row.qualif, function (i, item) {
                            calif += parseFloat(item.calif);
                        });
                        var result = (calif / row.qualif.length).toFixed(2) >= 7;
                        if (result) {
                            return '<span class="badge badge-success">Aprobado</span>';
                        }
                        return '<span class="badge badge-danger">Repprobado</span>';
                    }
                },
            ],
            initComplete: function (settings, json) {
                $('.btnRemoveNotes').prop('disabled', json.length === 0);
            },
        });
    });
});