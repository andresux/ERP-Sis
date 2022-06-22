var tblPermissions;
var items = {
    details: {
        name: "",
        permissions: [],
    },
    listAll: function () {
        tblPermissions = $('#tblPermissions').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.permissions,
            lengthChange: false,
            bPaginate: false,
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "state"},
            ],
            columnDefs: [
                {
                    targets: ['_all'],
                    orderable: false
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        var html = "";
                        $.each(row.permissions, function (i, item) {
                            var attr = item.state === 1 ? " checked" : "";
                            html += '<div class="form-check form-check-inline">';
                            html += '<input class="form-check-input" type="checkbox" data-id="' + item.id + '" data-pos="' + item.pos + '" name="chkperm"' + attr + '>';
                            html += '<label class="form-check-label">'+item.name+'</label>';
                            html += '</div>';
                        });
                        return html;
                    }
                },
            ],
            order: [[0, 'asc']]
        });
    },
};

$(function () {

    $('#tblPermissions tbody')
        .on('change', 'input[type="checkbox"][name="chkperm"]', function () {
        var id = parseInt($(this).data('id'));
        var pos = parseInt($(this).data('pos'));
        var td = tblPermissions.cell($(this).closest('td, li')).index(),
            row = tblPermissions.row(td.row).data();
        permission = row.permissions.filter(function (value, index) {
            return value.id === id;
        });
        row.permissions[pos].state = this.checked ? 1 : 0;
        console.log(tblPermissions.row(td.row).data());
    });

    $('input[type="checkbox"][name="chkstateall_perm"]')
        .on('change', function () {
        var state = this.checked;
        var cells = tblPermissions.cells().nodes();
        $(cells).find('input[type="checkbox"][name="chkperm"]').prop('checked', state).change();
    });

});

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmGroup');
    const fv = FormValidation.formValidation(form, {
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
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            // Send { username: 'its value', email: 'its value' } to the back-end
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="name"]').value,
                                    id: form.querySelector('[name="id"]').value,
                                    type: 'name',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
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
            const submitButton = fv.form.querySelector('[type="submit"]');
            submitButton.removeAttribute('disabled');
            items.details.permissions = [];

            $.each(tblPermissions.rows().data(), function (i, item) {
                var permissions = item.permissions.filter(function (value, key) {
                    return value.state === 1;
                });
                $.each(permissions, function (k, v) {
                    items.details.permissions.push(v);
                });
            });

            if (items.details.permissions.length === 0) {
                message_error('Debe seleccionar al menos un permiso');
                return false;
            }

            var parameters = {
                action: $('input[name="action"]').val(),
                id: $('input[name="id"]').val(),
                name: $('input[name="name"]').val(),
                items: JSON.stringify(items.details)
            };

            var msg = (parameters.action === 'add') ? 'guardar':'editar';

            dialog_submit_to_ajax('Notificación',
                '¿Deseas '+msg+' el siguiente registro?',
                pathname,
                parameters,
                function () {
                    location.href = form.getAttribute('data-url');
                }
            )
        });
});



