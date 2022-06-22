var fv;
$(function () {
    $('input[name="name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
});

$( document ).ready(function() {
    const csrftoken = getCookie('csrftoken');
    let data = [];
    let global_course = $("#course").val()!=""?$("#course").val():0;

    
    function submit_formdata_ajax_no_redirect(fv) {
        var form = fv.form;
        var submitButton = fv.form.querySelector('[type="submit"]');
        var parameters = new FormData($(form)[0]);
        $.confirm({
            type: 'blue',
            theme: 'material',
            title: 'Confirmación',
            icon: 'fa fa-info',
            content: '¿Esta seguro de guardar el siguiente registro?',
            columnClass: 'small',
            typeAnimated: true,
            cancelButtonClass: 'btn-primary',
            draggable: true,
            dragWindowBorder: false,
            buttons: {
                info: {
                    text: "Si",
                    btnClass: 'btn-primary',
                    action: function () {
                        $.ajax({
                            url: pathname,
                            data: parameters,
                            method: 'POST',
                            dataType: 'json',
                            processData: false,
                            contentType: false,
                            success: function (request) {
                                console.log(request);
                                if (!request.hasOwnProperty('error')) {
                                    location.href = "/college/report/final/"+request.id+"/"
                                    return false;
                                }
                                message_error(request.error);
                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                message_error(errorThrown + ' ' + textStatus);
                            }
                        });
                    }
                },
                danger: {
                    text: "No",
                    btnClass: 'btn-red',
                    action: function () {
                        if(submitButton != null){
                            submitButton.removeAttribute('disabled');
                        }
                    }
                },
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i of cookies) {
                const cookie = i.trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function change_course(id){        
        if(id != ""){
            let request = new Request(
                "/college/api/get_matters_by_course",
                {
                    method: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    mode: 'same-origin',
                    json: true,
                    body: JSON.stringify({"course": id})
                }
            );
            fetch(request)
            .then(response => response.json())
            .then(res => {
                var options = "";
                $.each(res.data, function() {
                    options += `<option value="${this["mat_id"]}">${this["mat_name"]}</option>`;
                });
                $("#id_matter").html(options);
            })
        }else{
            $("#id_matter").html("")
        }
    }

    $("#course").change(function(){
        change_course($(this).val());
    });

    $("#btn_submit").click(function(e){
        fv.validate().then(function(status) {
            console.log(status)
        });
        e.preventDefault();
    });

    change_course($("#course").val());

    
    const isNotEmpty = function() {
        return {
            validate: function (input) {
                const value = input.value;
                if (value === '') {
                    return {
                        valid: false,
                    };
                }
                return {
                    valid: true,
                };
            },
        };
    };
    FormValidation.validators.validSelect = isNotEmpty;

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
                            message: 'El nombre del curso es requerido'
                        }
                    }
                },
                matter: {
                    validators: {
                        notEmpty: {                        
                            message: 'El nombre de la materia es requerido'
                        }
                    }
                },
                teacher: {
                    validators: {
                        notEmpty: {                        
                            message: 'La materia no cuenta con profesor'
                        }
                    }
                },
                coordinator: {
                    validators: {
                        notEmpty: {                        
                            message: 'Coordinadora es requerido'
                        }
                    }
                },
                total_hours: {
                    validators: {
                        notEmpty: {                        
                            message: 'El número total de horas es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
                        }
                    }
                },
                folio: {
                    validators: {
                        notEmpty: {                        
                            message: 'El folio es requerido'
                        }
                    }
                },
                subject: {
                    validators: {
                        notEmpty: {                        
                            message: 'El tema es requerido'
                        }
                    }
                },
                modality: {
                    validators: {
                        notEmpty: {                        
                            message: 'La modalidad es requerida'
                        }
                    }
                },
                via: {
                    validators: {
                        notEmpty: {                        
                            message: 'La ubicación/plataforma es requerida'
                        }
                    }
                },
                class_hours: {
                    validators: {
                        notEmpty: {                        
                            message: 'El número de horas clase es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
                        }
                    }
                },
                self_hours: {
                    validators: {
                        notEmpty: {                        
                            message: 'El número de horas clase es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
                        }
                    }
                },
                imparted_hours: {
                    validators: {
                        notEmpty: {                        
                            message: 'El número de horas impartidas es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
                        }
                    }
                },
                documents_type: {
                    validators: {
                        notEmpty: {
                            message: 'Debe llenar el campo Documentos o anexos'
                        }
                    }
                }
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
        submit_formdata_ajax_no_redirect(fv);
    });

});