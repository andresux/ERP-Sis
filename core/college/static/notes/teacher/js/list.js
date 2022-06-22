var id = 0;
var tblNotes;

$(function () {
    $('#data tbody').on('click', 'a[rel="notes"]', function () {
        $('.tooltip').remove();
        id = $(this).data('id');
        tblNotes = $('#tblNotes').DataTable({
            responsive: true,
            autoWidth: true,
            // scrollX: true,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_notes',
                    'id': id
                },
                dataSrc: ""
            },
            columns: [
                {data: "matr.student.user.full_name"},
                {data: "lesson1"},
                {data: "lesson2"},
                {data: "lesson3"},
                {data: "lesson4"},
                {data: "exam"},
                {data: "average"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, -5, -6, -7],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var result = parseFloat(row.average) >= 7;
                        if (result) {
                            return '<span class="badge badge-success">Aprobado</span>';
                        }
                        return '<span class="badge badge-warning">Reprobado</span>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (parseFloat(data.average) < 7.00) {
                    $(tr).css({'background': '#dc3345', 'color': 'white'});
                }
            },
            initComplete: function (settings, json) {
                $('.btnRemoveNotes').prop('disabled', json.length === 0);
            },
        });
        $('#myModalNotes').modal('show');
    });

    $('.btnRemoveNotes').on('click', function () {
        // var ids = [];
        // $.each(tblNotes.rows().data().toArray(), function (key, value) {
        //     $.each(value.qualif, function (i, item) {
        //         ids.push(item.id);
        //     });
        // });

        dialog_submit_to_ajax('Notificación',
            '¿Estas seguro de eliminar las notas de esta materia?',
            pathname,
            {
                'action': 'remove_notes',
                'id': id
            },
            function () {
                location.reload();
            },
        );
    });
});