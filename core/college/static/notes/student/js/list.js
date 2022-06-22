var select_course;
var tblNotes;
var btnPrint;

$(function () {
    select_course = $('select[name="course"]');
    btnPrint = $('.btnPrint');
    btnPrint.prop('disabled', true);

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_course.on('change', function () {
        btnPrint.prop('disabled', select_course.val() === '');
        if (select_course.val() === '') {
            if (tblNotes != null) tblNotes.clear().draw();
            return false;
        }
        tblNotes = $('#tblNotes').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering: false,
            lengthChange: false,
            searching: true,
            paginate: false,
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
                {data: "teach_cours_mat.course_mat.mat.name"},
                {data: "teach_cours_mat.teacher_mat.teacher.user.full_name"},
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
            initComplete: function (settings, json) {
                btnPrint.prop('disabled', json.length === 0);
            },
        });
    });

    btnPrint.on('click', function () {
        window.open(pathname + 'print/' + select_course.val());
    });

    select_course.val('').change();
});