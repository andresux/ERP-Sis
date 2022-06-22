var select_period;
var select_teacher;
var tblMattersSearch;
var btnSearchMat;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmCourse');
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
                period: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un periodo escolar'
                        },
                    }
                },
                teacher: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un docente'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    teacher: form.querySelector('[name="teacher"]').value,
                                    period: form.querySelector('[name="period"]').value,
                                    id: form.querySelector('[name="id"]').value,
                                    action: 'validate_data'
                                };
                            },
                            message: 'Ya se registro las materias con el docente y periodo seleccionado',
                            method: 'POST'
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
            items.details.teacher = select_teacher.val();
            items.details.period = select_period.val();

            if (items.details.matters.length === 0) {
                message_error('Debe tener al menos un item en el detalle de las materias');
                return false;
            }

            dialog_submit_to_ajax('Notificación',
                '¿Estas seguro de guardar las siguientes materias con el docente seleccionado?',
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

var items = {
    details: {
        name: '',
        period: '',
        teacher: '',
        matters: []
    },
    get_matter_ids: function () {
        var ids = [];
        $.each(this.details.matters, function (i, item) {
            ids.push(item.id);
        });
        return ids;
    },
    list_matters: function () {
        $.each(this.details.matters, function (i, item) {
            item.pos = i;
        });
        tblMatters = $('#tblMatters').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.matters,
            ordering: false,
            lengthChange: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "mat.name"},
                {data: "course.classroom.name"},
                {data: "course.level"},
                {data: "course.period.name"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x" aria-hidden="true"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {

            },
        });
    },
    add_matter: function (item) {
        this.details.matters.push(item);
        this.list_matters();
    }
};

$(function () {
    // declarative variables
    btnSearchMat = $('.btnSearchMat');
    btnSearchMat.prop('disabled', true);
    select_period = $('select[name="period"]');
    select_teacher = $('select[name="teacher"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_period
        .on('change.select2', function () {
            fv.revalidateField('period');
            fv.revalidateField('teacher').then(function (status) {
                btnSearchMat.prop('disabled', status === 'Invalid');
            });
            btnSearchMat.prop('disabled', select_period.val() === '');
            items.details.matters = [];
            items.list_matters();
        });

    select_teacher
        .on('change.select2', function () {
            fv.revalidateField('teacher').then(function (status) {
                btnSearchMat.prop('disabled', status === 'Invalid');
            });
        });

    btnSearchMat.on('click', function () {
        if (select_period.val() === '') {
            message_error('Debe seleccionar un perido');
            return false;
        }

        tblMattersSearch = $('#tblMattersSearch').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_matters',
                    'period': select_period.val(),
                    'ids': JSON.stringify(items.get_matter_ids())
                },
                dataSrc: ''
            },
            columns: [
                {"data": "mat.name"},
                {"data": "course.classroom.name"},
                {"data": "course.level"},
                {"data": "course.period.name"},
                {"data": "state"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.state) {
                            return '<i class="fas fa-calendar-times"></i>';
                        }
                        return '<a rel="add" class="btn btn-success btn-xs"><i class="fas fa-calendar-check"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-danger">Ocupada</span>';
                        }
                        return '<span class="badge badge-success">Libre</span>';
                    }
                },
            ],
        });
        $('#myModalMatters').modal('show');
    });

    $('.btnRemoveAllMat').on('click', function () {
        if (items.details.matters.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            items.details.matters = [];
            items.list_matters();
        });
    });

    $('#tblMatters tbody')
        .on('click', 'a[rel="remove"]', function () {
            var td = tblMatters.cell($(this).closest('td, li')).index();
            var row = tblMatters.row(td.row).data();
            items.details.matters.splice(row.pos, 1);
            items.list_matters();
        });

    $('#tblMattersSearch tbody').on('click', 'a[rel="add"]', function () {
        var row = tblMattersSearch.row($(this).parents('tr')).data();
        items.add_matter(row);
        tblMattersSearch.row($(this).parents('tr')).remove().draw();
    });

    if (select_period.val() !== '') {
        select_period.change();
    }

    items.details.matters = matters;
    items.list_matters();
});