var select_course;
var select_matter;
var tblStudents = null;

function getStudents() {
    var parameters = {
        'action': 'search_students',
        'id': select_matter.val(),
        'course': select_course.val(),
    };

    if ($.isEmptyObject(parameters.id) || $.isEmptyObject(parameters.course)) {
        clearTable();
        return false;
    }

    tblStudents = $('#tblStudents').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        columns: [
            {data: "student.user.username"},
            {data: "student.user.first_name"},
            {data: "student.user.last_name"},
            {data: "student.user.email"},
            {data: "student.user.dni"},
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
        ],
        columnDefs: []
    });
}

function clearTable() {
    if (tblStudents !== null) {
        tblStudents.clear().draw();
    }
}

function clearSelect(select) {
    var items = [{'id': '', 'text': '--------------'}];
    select.html('').select2({
        data: items,
        theme: 'bootstrap4',
        language: "es"
    });
}

$(function () {

    select_course = $('select[name="course"]');
    select_matter = $('select[name="matter"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_course.on('change', function () {
        var id = $(this).val();
        clearSelect(select_matter);
        clearTable();
        if ($.isEmptyObject(id)) return false;
        $.ajax({
            url: pathname,
            data: {
                'action': 'search_matter',
                'course': id
            },
            type: 'POST',
            dataType: 'json',
            beforeSend: function () {

            },
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    var items = request;
                    items.unshift({'id': '', 'text': '------------'});
                    select_matter.html('').select2({
                        data: items,
                        theme: 'bootstrap4',
                        language: "es"
                    });
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            },
            complete: function () {

            }
        });
    });

    select_matter.on('change', function () {
        getStudents();
    });
});