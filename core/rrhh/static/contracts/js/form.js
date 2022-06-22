var defaultDate;
var fv;
var input_enddate;
var input_startdate;

$(function () {

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('select[name="emp"]')
        .on('change.select2', function () {
            fv.revalidateField('emp');
        });

    $('select[name="job"]')
        .on('change.select2', function () {
            fv.revalidateField('job');
        });

    $('[name="rmu"]').TouchSpin({
        min: 0,
        max: 100000,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        verticalbuttons: true,
        verticalupclass: 'glyphicon glyphicon-plus',
        verticaldownclass: 'glyphicon glyphicon-minus'
    }).keypress(function (e) {
        return validate_decimals($(this), e);
    });

    defaultDate = new moment().format("YYYY-MM-DD");
    input_enddate = $('input[name="end_date"]');
    input_startdate = $('input[name="start_date"]');

    input_enddate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        minDate: defaultDate
    });

    input_enddate.datetimepicker('date', input_enddate.val());

    input_startdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        minDate: defaultDate
    });

    input_startdate.datetimepicker('date', input_startdate.val());

    input_startdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('start_date');
        input_endate.datetimepicker('minDate', e.date);
        input_endate.datetimepicker('date', e.date);
    });

    input_enddate.on('change.datetimepicker', function (e) {
        fv.revalidateField('end_date');
    });
});

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
                rmu: {
                    validators: {
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        }
                    }
                },
                emp: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un empleado'
                        },
                    }
                },
                job: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un cargo'
                        },
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
