var type = null,
    month = null,
    year = null,
    action = null;

var fv;
var input_year;
var select_month;

function generate_rol() {
    year = input_year.val();
    month = $('select[name="month"]').val();

    if (year === "" || month === "") {
        tblRolPay.clear().draw();
        return false;
    }

    tblRolPay = $('#tblSalary').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                action: 'generate',
                year: year,
                month: month
            },
            dataSrc: ""
        },
        columns: [
            {"data": "cont.emp.user.full_name"},
            {"data": "cont.job.name"},
            {"data": "cont.rmu"},
            {"data": "dias_lab"},
            {"data": "daysalary"},
            {"data": "salary_dayslab"},
            {"data": "ingress"},
            {"data": "egress"},
            {"data": "total"},
        ],
        columnDefs: [
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [-1, -4, -5, -7],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<a rel="dsctos" data-type="1" class="text-danger" style="cursor: pointer;">$' + row.ingress + '</a>';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<a rel="dsctos" data-type="2" class="text-primary" style="cursor: pointer;">$' + row.egress + '</a>';
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    tblRolPay = $('.table').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true
    });

    input_year = $('input[name="year"]');
    select_month = $('select[name="month"]');

    input_year.datetimepicker({
        locale: 'es',
        keepOpen: false,
        viewMode: 'years',
        format: 'YYYY'
    });

    input_year.datetimepicker('date', new moment().format('YYYY'));

    input_year.on('change.datetimepicker', function (e) {
        fv.revalidateField('month');
        fv.revalidateField('year');
        generate_rol();
    });

    $('#tblSalary tbody').on('click', 'a[rel="dsctos"]', function () {
        $('.tooltip').remove();
        var td = tblRolPay.cell($(this).closest('td, li')).index(),
            rows = tblRolPay.row(td.row).data();
        var type = parseInt($(this).data('type'));
        $('#tblDsctos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering: false,
            lengthChange: false,
            paging: false,
            data: rows.details.filter(function (item, key) {
                return item.type_id === type
            }),
            columns: [
                {"data": "name"},
                {"data": "calculation"},
                {"data": "valor"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data + '%';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ]
        });
        $('#myModalDsctos').modal('show');
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_month
        .on('change.select2', function () {
            generate_rol();
            fv.revalidateField('month');
            fv.revalidateField('year');
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmRolPay');
    fv = FormValidation.formValidation(form, {
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
                year: {
                    validators: {
                        notEmpty: {},
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    month: form.querySelector('[name="month"]').value,
                                    year: form.querySelector('[name="year"]').value,
                                    type: 'name',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El rol de pago ya se encuentra registrado',
                            method: 'POST'
                        }
                    },
                },
                month: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un mes'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    month: form.querySelector('[name="month"]').value,
                                    year: form.querySelector('[name="year"]').value,
                                    type: 'name',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El rol de pago ya se encuentra registrado',
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
            var url_refresh = form.getAttribute('data-url');

            var parameters = {
                'action': 'create',
                'year': $('input[name="year"]').val(),
                'month': $('select[name="month"]').val(),
            };

            dialog_submit_to_ajax('Notificación',
                '¿Estas seguro de guardar el siguiente rol de pago?',
                pathname,
                parameters,
                function () {
                    location.href = url_refresh;
                }
            );
        });
});
