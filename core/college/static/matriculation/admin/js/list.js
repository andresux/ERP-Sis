var fvStateMat;
var matr;
var select_state;

document.addEventListener('DOMContentLoaded', function (event) {
    const form = document.getElementById('frmStateMat');
    fvStateMat = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                state: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un estado'
                        },
                    }
                }
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
            const iconPlugin = fvStateMat.getPlugin('icon');
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
            dialog_submit_to_ajax('Alerta',
                '¿Estas seguro de editar el estado de la matricula?',
                pathname, {
                    'action': 'edit_statemat',
                    'id': matr,
                    'state': select_state.val()
                }, function () {
                    alert_sweetalert('success', 'Notificación', 'Se cambio correctamente el estado de la matricula', function () {
                        location.reload();
                    }, 1500, null);
                });
        });
});


$(function () {

    select_state = $('select[name="state"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_state
        .on('change.select2', function () {
            fvStateMat.revalidateField('state');
        });

    $('#myModalStateMat').on('hidden.bs.modal', function () {
        select_state.val('').change();
    });

    $('#data tbody')
        .on('click', 'a[rel="matters"]', function () {
            $('.tooltip').remove();
            var td = table.cell($(this).closest('td, li')).index(),
                rows = table.row(td.row).data();
            var id = parseInt(rows[0]);
            $('#tblMatters').DataTable({
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
                        'id': id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "name"},
                    {data: "teacher"},
                ],
                columnDefs: []
            });
            $('#myModalMatters').modal('show');
        })
        .on('click', 'a[rel="state"]', function () {
            $('.tooltip').remove();
            var td = table.cell($(this).closest('td, li')).index(),
                rows = table.row(td.row).data();
            matr = parseInt(rows[0]);
            fvStateMat.resetForm(true);
            $('#myModalStateMat').modal('show');
        });
});