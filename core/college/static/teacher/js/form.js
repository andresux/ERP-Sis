var input_birthdate;
var fv;
var select_typeemp;
var frmGroups;

document.addEventListener('DOMContentLoaded', function (event) {
    const form = document.getElementById('frmForm');
    fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                // defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
                excluded: new FormValidation.plugins.Excluded(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                first_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        },
                        regexp: {
                            regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                            message: 'Debe ingresar sus dos nombres y solo utilizando caracteres alfabéticos'
                        },
                    }
                },
                last_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        },
                        regexp: {
                            regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                            message: 'Debe ingresar sus dos apellidos y solo utilizando caracteres alfabéticos'
                        },
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10,
                        },
                        digits: {},
                        callback: {
                            message: 'Introduce un número de cedula válido',
                            callback: function (input) {
                                return validate_dni_ruc(input.value);
                            }
                        },
                        remote: {
                            url: pathname,
                            // Send { username: 'its value', email: 'its value' } to the back-end
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="dni"]').value,
                                    id: form.querySelector('[name="id"]').value,
                                    type: 'dni',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El número de cedula ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10,
                        },
                    }
                },
                conventional: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 7,
                        },
                        digits: {},
                    }
                },
                email: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El email no es correcto'
                        },
                        remote: {
                            url: pathname,
                            // Send { username: 'its value', email: 'its value' } to the back-end
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="email"]').value,
                                    id: form.querySelector('[name="id"]').value,
                                    type: 'email',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El email ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                profession: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una profesión'
                        }
                    }
                },
                prof: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una profesión'
                        }
                    }
                },
                address: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                gender: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un genero',
                        },
                    }
                },
                birthdate: {
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
                cvitae: {
                    validators: {
                        // file: {
                        //     extension: 'application/pdf',
                        //     type: 'pdf',
                        //     maxFiles: 1,
                        //     message: 'Introduce un documento pdf válido'
                        // }
                    }
                },
            }
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

function validateTypeEmp() {
    var type = select_typeemp.val();
    $(frmGroups[11]).hide();
    $(frmGroups[12]).hide();
    switch (type) {
        case 'docente':
            $(frmGroups[11]).show();
            $(frmGroups[12]).show();
            break;
    }
}

$(function () {

    input_birthdate = $('input[name="birthdate"]');
    select_typeemp = $('select[name="type"]');
    frmGroups = $('#frmForm .form-group');

    validateTypeEmp();

    $('[name="mobile"]').intlTelInput({
        utilsScript: '/static/lib/intl-tel-input-11.1.2/js/utils.js',
        autoPlaceholder: true,
        initialCountry: 'ec',
        onlyCountries: ["ec"],
        formatOnDisplay: false,
        allowDropdown: false
    });

    input_birthdate.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        defaultDate: new moment().format("YYYY-MM-DD")
    });

    input_birthdate.datetimepicker('date', input_birthdate.val());

    input_birthdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('birthdate');
    });

    $('input[name="dni"]', 'input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    // select_typeemp
    //     .on('change.select2', function () {
    //         fv.revalidateField('type');
    //         validateTypeEmp();
    //     });

    $('select[name="gender"]')
        .on('change.select2', function () {
            fv.revalidateField('gender');
        });

    $('select[name="profession"]')
        .on('change.select2', function () {
            fv.revalidateField('profession');
        });

    // $(fv.form).find('input[name="first_name"]').val('Jorge Luis');
    // $(fv.form).find('input[name="last_name"]').val('Merchán Freire');
    // $(fv.form).find('input[name="dni"]').val('0302660881');
    // $(fv.form).find('input[name="email"]').val('jorgeluis1994@hotmail.com');
    // $(fv.form).find('select[name="type"]').val('estudiante').trigger('change');
    // $(fv.form).find('select[name="gender"]').val('1').trigger('change');
    // $(fv.form).find('input[name="address"]').val('Vargas torres');
    // $(fv.form).find('input[name="mobile"]').val('0979014551');
    // $(fv.form).find('input[name="conventional"]').val('2977557');
    // $(fv.form).find('select[name="prof"]').val('docente').trigger('change');
});