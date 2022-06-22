var fv;
$(function () {
    $('input[name="name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
});

$( document ).ready(function() {
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
                matter: {
                    validators: {
                        notEmpty: {                        
                            message: 'El nombre de la materia es requerido'
                        }
                    }
                },
                name: {
                    validators: {
                        notEmpty: {                        
                            message: 'El nombre de la unidad es requerido'
                        }
                    }
                },
                number: {
                    validators: {
                        notEmpty: {                        
                            message: 'El número de unidad es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
                        }
                    }
                },
                total_hours: {
                    validators: {
                        notEmpty: {                        
                            message: 'El número de unidad es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
                        }
                    }
                },
                learning_result: {
                    validators: {
                        notEmpty: {
                            message: 'Los resultados de aprendizaje son requeridos'
                        }
                    }
                },
                presencial_hours: {
                    validators: {
                        notEmpty: {
                            message: 'El número de horas presenciales es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
                        }
                    }
                },
                virtual_hours: {
                    validators: {
                        notEmpty: {                        
                            message: 'El número de horas virtuales es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
                        }
                    }
                },
                self_hours: {
                    validators: {
                        notEmpty: {                        
                            message: 'El número de horas autónomas es requerido'
                        },
                        digits: {                        
                            message: 'Debe ingresar únicamente números'
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


    $(".btn-submit").click(function() {
        get_folios();
        $("#folios").val(JSON.stringify(foliosArray));
        if($(this).attr('id') == 'add_new'){
            $("#frmForm").attr('data-url',"/college/unit/add/");
        }else{
            $("#frmForm").attr('data-url',"/college/unit/");
        }
        fv.validate().then(function(status) {
            console.log(status)
        });
    });
    /* FOLIOS */

    let foliosArray = $("#folios").val() != ''? JSON.parse($("#folios").val()): []

    function load_folios(){
        let foliosData ="";
        for(let i = 0; i<foliosArray.length;i++){
            foliosData += `
            <h5>Folio ${i+1} </h5>
            <div id="folio${i}">
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label">Contenido:</label>
                    <div class="col-sm-10">            
                        <input type="text" value="${foliosArray[i]["contenido"]}" id="contenido${i}" placeholder="Ingrese contenido del folio" autocomplete="off" class="form-control" required>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label">Nombre folio:</label>
                    <div class="col-sm-10">            
                        <input type="text" value="${foliosArray[i]["nombre"]}" id="nombre${i}" placeholder="Ingrese nombre del folio" autocomplete="off" class="form-control" required>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label">Actividades de aprendizaje:</label>
                    <div class="col-sm-10">            
                        <input type="text" value="${foliosArray[i]["aprendizaje"]}" id="aprendizaje${i}" placeholder="Ingrese las actividades de aprendizaje del folio" autocomplete="off" class="form-control" required>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label">Actividades de evaluación:</label>
                    <div class="col-sm-10">            
                        <input type="text" value="${foliosArray[i]["evaluacion"]}" id="evaluacion${i}" placeholder="Ingrese las actividades de evaluación del folio" autocomplete="off" class="form-control" required>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label">Actividades autónomas:</label>
                    <div class="col-sm-10">
                        <input type="text" value="${foliosArray[i]["autonomas"]}" id="autonomas${i}" placeholder="Ingrese las actividades autónomas del folio" autocomplete="off" class="form-control" required>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label">Bibliografía básica:</label>
                    <div class="col-sm-10">
                    <input type="text" value="${foliosArray[i]["biblio-basica"]}" id="basica${i}" placeholder="Ingrese el link a la biografía" autocomplete="off" class="form-control" required>                        
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label">Bibliografía complementaria:</label>
                    <div class="col-sm-10">
                        <input type="text" value="${foliosArray[i]["biblio-complementaria"]}" id="complementaria${i}" placeholder="Ingrese el link a la biografía" autocomplete="off" class="form-control" required>
                    </div>
                </div>
                <div class="form-group row btn-right">
                    <a href="#" id="folio-${i}" class="btn btn-danger btn-flat folio-rm">
                        <i class="fas fa-minus-circle" aria-hidden="true"></i> Remover folio ${i+1}
                    </a>
                </div>
            </div>`;
        }
        foliosData += `
        <a href="#" id="addFolio" class="btn btn-primary btn-block btn-flat folio-add">
            <i class="fas fa-plus-circle" aria-hidden="true"></i> Agregar folio
        </a>`;
        $("#folioContainer").html(foliosData)
    }
    load_folios();

    $("#folioContainer").on( "click", "#addFolio", function() {
        get_folios();
        foliosArray.push({
            "contenido": "",
            "nombre": "",
            "aprendizaje": "",
            "evaluacion": "",
            "autonomas": "",
            "biblio-basica": "",
            "biblio-complementaria": ""
        });
        load_folios();
        return false;
    });

    function get_folios(){
        
        let foliosArrayTemp = []
        for(let i = 0; i<foliosArray.length;i++){
            if($(`#folio${i}`).length){
                foliosArrayTemp.push({
                    "contenido": $(`#contenido${i}`).val(),
                    "nombre": $(`#nombre${i}`).val(),
                    "aprendizaje": $(`#aprendizaje${i}`).val(),
                    "evaluacion": $(`#evaluacion${i}`).val(),
                    "autonomas": $(`#autonomas${i}`).val(),
                    "biblio-basica": $(`#basica${i}`).val(),
                    "biblio-complementaria": $(`#complementaria${i}`).val()
                })
            }else{
                console.log(`no existe`)
                break
            }
        }
        foliosArray = foliosArrayTemp;
    }

    $("#folioContainer").on( "click", ".folio-rm", function() {
        get_folios();
        foliosArray.splice($(this).attr("id").split("-")[1], 1)
        $("#"+$(this).attr("id")).remove();
        load_folios();
        return false;
    });
    
});
/* END FOLIOS */