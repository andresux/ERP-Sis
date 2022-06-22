var fv;

$(function () {

    $('[name="mobile"]').intlTelInput({
        utilsScript: '/static/lib/intl-tel-input-11.1.2/js/utils.js',
        autoPlaceholder: true,
        initialCountry: 'ec',
        onlyCountries: ["ec"],
        formatOnDisplay: false,
        allowDropdown: false
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="layout"]')
        .on('change.select2', function () {
            fv.revalidateField('layout');
        });

    $('select[name="template"]')
        .on('change.select2', function () {
            fv.revalidateField('template');
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
            },
            fields: {
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        },
                    }
                },
                system_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        },
                    }
                },
                icon: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        },
                    }
                },
                image: {
                    notEmpty: {},
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                proprietor: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        },
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
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10,
                        },
                        callback: {
                            message: 'El número de celular no es válido',
                            callback: function (input) {
                                return input.value === '' || input.intlTelInput('isValidNumber');
                            }
                        }
                    }
                },
                phone: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 7,
                        },
                        digits: {}
                    }
                },
                address: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                mission: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                vision: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                about_us: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                ruc: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 13,
                        },
                        digits: {},
                        callback: {
                            message: 'Introduce un número de cedula o ruc válido',
                            callback: function (input) {
                                return validate_dni_ruc(input.value);
                            }
                        },
                    }
                },
                layout: {
                    validators: {
                        notEmpty: {},
                    }
                },
                card: {
                    validators: {
                        notEmpty: {},
                    }
                },
                navbar: {
                    validators: {
                        notEmpty: {},
                    }
                },
                brand_logo: {
                    validators: {
                        notEmpty: {},
                    }
                },
                sidebar: {
                    validators: {
                        notEmpty: {},
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

