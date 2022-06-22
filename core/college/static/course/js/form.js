var fv;
var tblMatters;
var select_period;
var select_level;
var select_classroom;
var items = {
    details: {
        classroom: '',
        period: '',
        level: '',
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
                {data: "name"},
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
                classroom: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un paralelo'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    classroom: form.querySelector('[name="classroom"]').value,
                                    period: form.querySelector('[name="period"]').value,
                                    level: form.querySelector('[name="level"]').value,
                                    id: form.querySelector('[name="id"]').value,
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre del curso ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                period: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un periodo escolar'
                        }
                    }
                },
                level: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un nivel escolar'
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

            items.details.classroom = select_classroom.val();
            items.details.period = select_period.val();
            items.details.level = select_level.val();

            if (items.details.matters.length === 0) {
                message_error('Debe tener al menos un item en el detalle del curso');
                return false;
            }

            dialog_submit_to_ajax('Notificación',
                '¿Estas seguro de guardar el siguiente curso?',
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

    // declarative variables
    select_period = $('select[name="period"]');
    select_level = $('select[name="level"]');
    select_classroom = $('select[name="classroom"]');

    $('input[name="name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_period
        .on('change.select2', function () {
            fv.revalidateField('period');
            fv.revalidateField('classroom');
        });

    select_level
        .on('change.select2', function () {
            fv.revalidateField('level');
            fv.revalidateField('classroom');
        });

    select_classroom
        .on('change.select2', function () {
            fv.revalidateField('classroom');
        });

    // Matters

    $("#search_mat").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_mat',
                    'term': request.term,
                    'ids': JSON.stringify(items.get_matter_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            items.add_matter(ui.item);
            $(this).val('').focus();
        }
    });

    $('#btnRemoveMatsAll').on('click', function () {
        if (items.details.matters.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos las materias de tu detalle?', function () {
            items.details.matters = [];
            items.list_matters();
        });
    });

    $('#clearSearchMat').on('click', function () {
        $('#search_mat').val('').focus();
    });

    $('#tblMatters tbody')
        .on('click', 'a[rel="remove"]', function () {
            var td = tblMatters.cell($(this).closest('td, li')).index();
            var row = tblMatters.row(td.row).data();
            items.details.matters.splice(row.pos, 1);
            items.list_matters();
        });
});
