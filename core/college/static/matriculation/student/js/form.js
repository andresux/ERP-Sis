var fv;
var select_course;
var tblMatters = null;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
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
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    course: form.querySelector('[name="course"]').value,
                                    action: 'validate_data'
                                };
                            },
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
            submit_formdata_ajax(fv);
        });
});

function loadMatters() {
    if (select_course.val() === '' && tblMatters != null) {
        tblMatters.clear().draw();
        return false;
    }

    tblMatters = $('#tblMatters').DataTable({
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
                'action': 'search_matters',
                'id': select_course.val()
            },
            dataSrc: ''
        },
        columns: [
            {"data": "name"},
            {"data": "teacher"},
        ],
        columnDefs: [],
    });
}

$(function () {
    select_course = $('select[name="course"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_course
        .on('change.select2', function () {
            if(tblMatters != null){
                tblMatters.clear().draw();
            }
            fv.revalidateField('course').then(function (status) {
                if(status.toLowerCase() === 'valid'){
                    loadMatters();
                }
            });
        });

    loadMatters();
});
