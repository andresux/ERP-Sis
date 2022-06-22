var select_course;
var select_matters;
var select_semester;
var tblNotes;
var fv;

var items = {
    details: {
        matter: '',
        course: '',
        notes: []
    }
};

function getNotes() {
    if (tblNotes != null) {
        tblNotes.clear().draw();
    }

    var course = select_course.val();
    if (course === '') {
        return false;
    }

    var matter = select_matters.val();
    if (matter === '') {
        return false;
    }

    tblNotes = $('#tblNotes').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                // 'semester': semester,
                'action': 'search_students_notes',
                'course': course,
                'matter': matter
            },
            dataSrc: ''
        },
        ordering: false,
        lengthChange: false,
        paginate: false,
        columns: [
            {data: "matr.student.user.full_name"},
            {data: "notes.lesson1"},
            {data: "notes.lesson2"},
            {data: "notes.lesson3"},
            {data: "notes.lesson4"},
            {data: "notes.exam"},
            {data: "notes.average"},
        ],
        columnDefs: [
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<input type="text" name="lesson1" class="form-control" value="' + row.notes.lesson1 + '" autocomplete="off">';
                }
            },
            {
                targets: [2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<input type="text" name="lesson2" class="form-control" value="' + row.notes.lesson2 + '" autocomplete="off">';
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<input type="text" name="lesson3" class="form-control" value="' + row.notes.lesson3 + '" autocomplete="off">';
                }
            },
            {
                targets: [4],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<input type="text" name="lesson4" class="form-control" value="' + row.notes.lesson4 + '" autocomplete="off">';
                }
            },
            {
                targets: [5],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<input type="text" name="exam" class="form-control" value="' + row.notes.exam + '" autocomplete="off">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(2);
                }
            },
        ],
        rowCallback: function (row, data, index) {
            var frm = $(row).closest('tr');

            frm.find('input').TouchSpin({
                min: 0.00,
                max: 10,
                step: 0.01,
                decimals: 2,
                boostat: 5,
                maxboostedstep: 10,
                //verticalbuttons: true
            }).keypress(function (e) {
                return validate_decimals($(this), e);
            });
        },
        initComplete: function (settings, json) {

        },
    });
}

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmNotes');
    fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                course: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un curso'
                        },
                    }
                },
                matters: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una materia'
                        }
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var refresh = form.getAttribute('data-url');
            items.details.notes = tblNotes.rows().data().toArray();
            items.details.matter = select_matters.val();
            items.details.course = select_course.val();

            dialog_submit_to_ajax('Notificación',
                '¿Estas seguro de guardar las siguientes notas?',
                pathname,
                {
                    'action': $('input[name="action"]').val(),
                    'id': $('input[name="id"]').val(),
                    'items': JSON.stringify(items.details)
                },
                function () {
                    location.href = refresh;
                },
            );
        });
});

$(function () {

    select_course = $('select[name="course"]');
    select_matters = $('select[name="matters"]');

    select_course.html('').select2({
        data: courses,
        theme: 'bootstrap4',
        language: "es"
    });

    select_course.on('change', function () {
        var options = [{'id': '', 'text': '--------'}];
        if (select_course.val() !== '') {
            var data = select_course.select2('data')[0].data;
            $.each(data, function (key, value) {
                options.push({
                    'id': value.id,
                    'text': value.course_mat.mat.name,
                    'data': value
                })
            });
        }

        select_matters.html('').select2({
            data: options,
            theme: 'bootstrap4',
            language: "es"
        });

        getNotes();
    });

    select_matters.on('change', function () {
        getNotes();
    });

    $('#tblNotes tbody')
        .on('change', 'input[name="lesson1"]', function () {
            var tr = tblNotes.cell($(this).closest('td, li')).index();
            var row = tblNotes.row(tr.row).data();
            row.notes.lesson1 = parseFloat($(this).val());
            row.notes.average = (parseFloat(row.notes.lesson1) + parseFloat(row.notes.lesson2) + parseFloat(row.notes.lesson3) + parseFloat(row.notes.lesson4) + parseFloat(row.notes.exam)) / 5;
            $('td:eq(6)', tblNotes.row(tr.row).node()).html(parseFloat(row.notes.average).toFixed(2));
        })
        .on('change', 'input[name="lesson2"]', function () {
            var tr = tblNotes.cell($(this).closest('td, li')).index();
            var row = tblNotes.row(tr.row).data();
            row.notes.lesson2 = parseFloat($(this).val());
            row.notes.average = (parseFloat(row.notes.lesson1) + parseFloat(row.notes.lesson2) + parseFloat(row.notes.lesson3) + parseFloat(row.notes.lesson4) + parseFloat(row.notes.exam)) / 5;
            $('td:eq(6)', tblNotes.row(tr.row).node()).html(parseFloat(row.notes.average).toFixed(2));
        })
        .on('change', 'input[name="lesson3"]', function () {
            var tr = tblNotes.cell($(this).closest('td, li')).index();
            var row = tblNotes.row(tr.row).data();
            row.notes.lesson3 = parseFloat($(this).val());
            row.notes.average = (parseFloat(row.notes.lesson1) + parseFloat(row.notes.lesson2) + parseFloat(row.notes.lesson3) + parseFloat(row.notes.lesson4) + parseFloat(row.notes.exam)) / 5;
            $('td:eq(6)', tblNotes.row(tr.row).node()).html(parseFloat(row.notes.average).toFixed(2));
        })
        .on('change', 'input[name="lesson4"]', function () {
            var tr = tblNotes.cell($(this).closest('td, li')).index();
            var row = tblNotes.row(tr.row).data();
            row.notes.lesson4 = parseFloat($(this).val());
            row.notes.average = (parseFloat(row.notes.lesson1) + parseFloat(row.notes.lesson2) + parseFloat(row.notes.lesson3) + parseFloat(row.notes.lesson4) + parseFloat(row.notes.exam)) / 5;
            $('td:eq(6)', tblNotes.row(tr.row).node()).html(parseFloat(row.notes.average).toFixed(2));
        })
        .on('change', 'input[name="exam"]', function () {
            var tr = tblNotes.cell($(this).closest('td, li')).index();
            var row = tblNotes.row(tr.row).data();
            row.notes.exam = parseFloat($(this).val());
            row.notes.average = (parseFloat(row.notes.lesson1) + parseFloat(row.notes.lesson2) + parseFloat(row.notes.lesson3) + parseFloat(row.notes.lesson4) + parseFloat(row.notes.exam)) / 5;
            $('td:eq(6)', tblNotes.row(tr.row).node()).html(parseFloat(row.notes.average).toFixed(2));
        });

    select_course.change();
});