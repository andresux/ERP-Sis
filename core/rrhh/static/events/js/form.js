var input_datejoined;
var defaultDate;
var fv;
var input_enddate;
var input_startdate;

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
                startEndDate: new FormValidation.plugins.StartEndDate({
                    format: 'YYYY-MM-DD',
                    startDate: {
                        field: 'start_date',
                        message: 'La fecha de inicio debe ser una fecha válida y anterior a la fecha de finalización'
                    },
                    endDate: {
                        field: 'end_date',
                        message: 'La fecha de finalización debe ser una fecha válida y posterior a la fecha de inicio'
                    },
                }),
            },
            fields: {
                details: {
                    validators: {
                        // notEmpty: {},
                        // stringLength: {
                        //     min: 2,
                        // },
                    }
                },
                cont: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un contrato'
                        }
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de evento'
                        }
                    }
                },
                start_date: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                end_date: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
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

$(function () {

    defaultDate = new moment().format("YYYY-MM-DD");
    input_enddate = $('input[name="end_date"]');
    input_startdate = $('input[name="start_date"]');

    input_enddate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        widgetPositioning: {
            horizontal: 'auto',
            vertical: 'bottom'
        }
        //minDate: defaultDate
    });

    input_enddate.datetimepicker('date', input_enddate.val());
    console.log(input_enddate.val());

    input_startdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        widgetPositioning: {
            horizontal: 'auto',
            vertical: 'bottom'
        }
        //minDate: defaultDate
    });

    input_startdate.datetimepicker('date', input_startdate.val());

    input_startdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('start_date');
        input_startdate.datetimepicker('minDate', e.date);
        input_enddate.datetimepicker('date', e.date);
    });

    input_enddate.on('change.datetimepicker', function (e) {
        fv.revalidateField('end_date');
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="cont"]')
        .on('change.select2', function () {
            fv.revalidateField('cont');
        });

    $('select[name="type"]')
        .on('change.select2', function () {
            fv.revalidateField('type');
        });

    // finish

});

