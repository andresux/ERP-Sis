var fv;
$(function () {
    $('input[name="name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });
});

$( document ).ready(function() {
    const csrftoken = getCookie('csrftoken');
    let folios = {};
    let data = [];
    let students = $("#assistance").val()!=""?JSON.parse($("#assistance").val()):{};
    let global_course = $("#course").val()!=""?$("#course").val():0;
    load_students();    
    load_anexos($(`#anexos`).val()!=""?JSON.parse($(`#anexos`).val()):[]);
    let global_folio = $("#folio_inicial").html();

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

    function load_folios(){
        let folios_selected = folios["mat-"+$("#id_matter").val()];
        if(folios_selected["lista"].length > 0){
            let options = "";
            for(let f of folios_selected["lista"]){
                options += `<option value="${f["nombre"]}">${f["nombre"]}</option>`;
            }
            $("#folio").html(options);
            load_data_folio();
        }else{
            $("#folio").html("");
            Swal.fire({
                type: 'error',
                title: 'Notificación',
                text: "La materia seleccionada no tiene folios agregados.",
            });
        }
    }

    function load_mat_data(){
        let foundData = data.find(element => element.mat_id == $("#id_matter").val());
        if(foundData != undefined){
            $("#teacher").val(foundData.teacher[0]+" "+foundData.teacher[1]);
        }else{
            $("#teacher").val("");
        }
    }


    function load_students(){
        if(students != null && students != undefined){
            let students_list = `<table style="width: 100%;">
                <tr>
                    <th>Nº</th>
                    <th>Cédula</th>
                    <th>Estudiantes</th>
                    <th>A</th>
                    <th>F</th>
                    <th>Observación</th>
                </tr>`;
            let number = 1;
            for(let s of Object.keys(students)){
                let item = students[s];
                students_list += `<tr>
                    <td>${number}</td>
                    <td>${item["cedula"]}</td>
                    <td>${item["nombre"]}</td>
                    <td><input type="radio" class="asistencia_radio" value="a" id="a-${item["id"]}" name="student-${item["id"]}" ${item["asistencia"]=='a'?'checked="true"':''}">A</td>
                    <td><input type="radio" class="asistencia_radio" value="f" id="f-${item["id"]}" name="student-${item["id"]}" ${item["asistencia"]=='f'?'checked="true"':''}">F</td>
                    <td><input type="text" id="studentobs-${item["id"]}" placeholder="" autocomplete="off" class="form-control" required="" value="${item["obs"]}"></td>
                </tr>`;
                number++;
            }
            students_list += `</table>`;
            $("#students_list").html(students_list);
        }
    }

    function load_data_folio(){
        let folios_selected = folios["mat-"+$("#id_matter").val()]["lista"].find(element => element.nombre == $("#folio").val());
        $("#content").val(folios_selected["contenido"]);
        $("#learning").val(folios_selected["aprendizaje"]);
        $("#self").val(folios_selected["autonomas"]);
        $("#evaluation").val(folios_selected["evaluacion"]);
        $("#total_hours").val(folios["mat-"+$("#id_matter").val()]["horas"]);
        if(global_folio != ""){
            $("#folio").val(global_folio);
            global_folio = "";
        }
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
                data = res.data;
                $("#id_matter").html(options);
                folios = res["folios"];
                load_folios();
                load_mat_data();
                if(global_course != id){
                    global_course = id;
                    students = {}
                    for(let s of data.find(element => element.mat_id == $("#id_matter").val())["students"]){
                        students["estudiante-"+s[0]] = {
                            "id": s[0],
                            "nombre": s[2] + " " +s[1],
                            "cedula": s[3],
                            "asistencia": "",
                            "obs": ""
                        }
                    }
                    load_students();
                }
            })
        }else{
            $("#id_matter").html("")
        }
    }

    $("#course").change(function(){
        change_course($(this).val());
    });

    $("#id_matter").change(function(){
        load_mat_data();
        load_folios();
    });

    $("#folio").change(function(){
        load_data_folio();
    });
    $("#students_list").on( "click", ".asistencia_radio", function() {
        let asis = $(this).attr("id").split("-");
        students["estudiante-"+asis[1]]["asistencia"] = asis[0];
    });

    function load_anexos(anexos){
        let anexos_list = "";
        let pos = 0;
        for(let a of anexos){
            anexos_list +=`<a href="#" class="anexos_rm" id="${pos}">
                <img class="rm_img" src="/static/img/default/empty.png">
                <img style='width:50px; height:50px;' src='${a}'>
            </a>`;
            pos++;
        }
        $(`#anexos_list`).html(anexos_list);
        $(`#anexos`).val(JSON.stringify(anexos));
    }

    $("#anexos_list").on( "click", ".anexos_rm", function() {
        if($(`#anexos`).val() != ""){
            let anexos = JSON.parse($(`#anexos`).val());
            anexos.splice($(this).attr("id"), 1);
            load_anexos(anexos);
        }
        return false;
    });    

    $("#btn_submit").click(function(e){
        let validate_assistance = true;
        for(let s of Object.keys(students)){
            if(students[s]["asistencia"] == ""){
                validate_assistance = false;
                break;
            }
            students[s]["obs"] = $("#studentobs-"+students[s]["id"]).val();
        }
        if(validate_assistance){
            $("#assistance").val(JSON.stringify(students));
        
            fv.validate().then(function(status) {
                console.log(status)
            });
        }else{
            Swal.fire({
                type: 'error',
                title: 'Notificación',
                text: "Existen estudiantes sin registro de asistencia.",
            });
        }
    });

    change_course($("#course").val());

    
    $(".upload-file").change(function() {
        var file = $(this)[0].files[0];
        var upload = new Upload(file);
        // check size or type here with upload.getSize() and upload.getType()
        upload.doUpload();
    });

    var Upload = function (file) {
        this.file = file;
    };
    
    Upload.prototype.getType = function() {
        return this.file.type;
    };
    Upload.prototype.getSize = function() {
        return this.file.size;
    };
    Upload.prototype.getName = function() {
        return this.file.name;
    };

    Upload.prototype.doUpload = function () {
        var formData = new FormData();
        formData.append("file", this.file);
        $.ajax({
            type: "POST",
            url: "/college/api/upload/",
            xhr: function () {
                var myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) {
                    myXhr.upload.addEventListener('progress', this.progressHandling, false);
                }
                return myXhr;
            },
            success: function(res) {
                let anexos = $(`#anexos`).val() != ""?JSON.parse($(`#anexos`).val()):[];
                anexos.push(res.url);
                load_anexos(anexos);
            },
            error: function (error) {
                Swal.fire({
                    type: 'error',
                    title: 'Notificación',
                    text: error.message,
                    grow: true,
                    timer: 2000
                });
            },
            async: true,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            timeout: 60000
        });
    }

    Upload.prototype.progressHandling = function (event) {
        var percent = 0;
        var position = event.loaded || event.position;
        var total = event.total;
        var progress_bar_id = `#progress`;
        if (event.lengthComputable) {
            percent = Math.ceil(position / total * 100);
        }
        // update progressbars classes so it fits your code
        $(progress_bar_id + " .progress-bar").css("width", +percent + "%");
        $(progress_bar_id + " .status").text(percent + "%");
    };

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
        submit_formdata_ajax(fv);
    });

});