var tblProducts,
    prov = null,
    product;
var fvIngress;
var fvProvider;
var input_datejoined;
var input_endate;
var pnlEndDate;
var select_typeproduct;
var defaultDate;
var items = {
    details: {
        prov: '',
        date_joined: '',
        end_date: '',
        subtotal: 0.00,
        iva: 0.00,
        dscto: 0.00,
        total: 0.00,
        payment: 0,
        products: [],
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        $.each(this.details.products, function (i, item) {
            item.pos = i;
            item.cant = parseInt(item.cant);
            item.subtotal = item.cant * parseFloat(item.cost);
            subtotal += item.subtotal;
        });
        console.log(subtotal);
        items.details.subtotal = subtotal;
        $('#subtotal').val(items.details.subtotal.toFixed(2));
    },
    add_totals: function () {
        tblProducts.row.add({
            cant: 0,
            cat: [],
            cost: '',
            id: 0,
            image: '',
            label: '',
            key: 'total',
            name: 'Total a pagar',
            pos: 0,
            price: '',
            state: false,
            stock: 0,
            subtotal: items.details.subtotal,
            value: ''
        }).draw(false);
    },
    list_products: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            ordering: false,
            lengthChange: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "cat.name"},
                {data: "cant"},
                {data: "cost"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '';
                        }
                        return data;
                    }
                },
                {
                    targets: [2],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '';
                        }
                        return data;
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '';
                        }
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if(!row.state){
                            return '<span name="'+row.key+'">$'+parseFloat(data).toFixed(2)+'</span>';
                        }
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '';
                        }
                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '';
                        }
                        return '---';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '';
                        }
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x" aria-hidden="true"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var frm = $(row).closest('tr');

                frm.find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 10000000,
                }).keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });

                // frm.find('input[name="cost"]').TouchSpin({
                //     min: 0.00,
                //     max: 1000000,
                //     step: 0.01,
                //     decimals: 2,
                //     boostat: 5,
                //     maxboostedstep: 10,
                // }).keypress(function (e) {
                //     return validate_decimals($(this), e);
                // });
            },
            initComplete: function (settings, json) {

            },
        });
        this.add_totals();
    },
    get_products_ids: function () {
        var ids = [];
        $.each(this.details.products, function (i, item) {
            ids.push(item.id);
        });
        return ids;
    },
    add_products: function (item) {
        this.details.products.push(item);
        this.list_products();
    },
};


document.addEventListener('DOMContentLoaded', function (e) {
    const frmIngress = document.getElementById('frmIngress');
    fvIngress = FormValidation.formValidation(frmIngress, {
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
                payment: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una forma de pago'
                        },
                    }
                },
                date_joined: {
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
            const iconPlugin = fvIngress.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmIngress.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var url_refresh = frmIngress.getAttribute('data-url');

            if (prov === null) {
                message_error('Debe tener un proveedor seleccionado');
                $('input[name="search_prov"]').focus().select();
                return false;
            }

            items.details.prov = prov.id;
            items.details.date_joined = $('input[name="date_joined"]').val();
            items.details.end_date = $('input[name="end_date"]').val();
            items.details.payment = parseInt($('select[name="payment"]').val());

            if (items.details.products.length === 0) {
                message_error('Debe tener al menos un item en el detalle de la compra');
                return false;
            }

            dialog_submit_to_ajax('Notificación',
                '¿Estas seguro de guardar la siguiente compra?',
                pathname,
                {
                    'action': $('input[name="action"]').val(),
                    'id': $('input[name="id"]').val(),
                    'items': JSON.stringify(items.details)
                },
                function () {
                    location.href = url_refresh;
                },
            );
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    const frmProvider = document.getElementById('frmProvider');
    fvProvider = FormValidation.formValidation(frmProvider, {
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
                            data: function () {
                                return {
                                    obj: frmProvider.querySelector('[name="name"]').value,
                                    id: 0,
                                    type: 'name',
                                    action: 'validate_prov'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                ruc: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 13
                        },
                        digits: {},
                        callback: {
                            message: 'Introduce un número de ruc es inválido',
                            callback: function (input) {
                                return validate_dni_ruc(input.value);
                            }
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: frmProvider.querySelector('[name="ruc"]').value,
                                    id: 0,
                                    type: 'ruc',
                                    action: 'validate_prov'
                                };
                            },
                            message: 'El número de ruc ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
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
                    }
                },
                address: {
                    validators: {
                        stringLength: {
                            min: 4,
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
            const iconPlugin = fvProvider.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmProvider.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            dialog_submit_to_ajax('Notificación', '¿Estas seguro de guardar el siguiente proveedor?', pathname,
                {
                    name: $('#id_name').val(),
                    mobile: $('#id_mobile').val(),
                    address: $('#id_address').val(),
                    email: $('#id_email').val(),
                    ruc: $('#id_ruc').val(),
                    action: 'create_prov'
                },
                function () {
                    $('#myModalAddProv').modal('hide');
                }
            );
        });
});


$(function () {

    pnlEndDate = $('#pnl_end_date');
    defaultDate = new moment().format("YYYY-MM-DD");
    input_datejoined = $('input[name="date_joined"]');
    input_endate = $('input[name="end_date"]');
    select_typeproduct = $('select[name="type_products"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('select[name="payment"]')
        .on('change.select2', function () {
            fvIngress.revalidateField('payment');
            var id = parseInt($(this).val());
            var start_date = input_datejoined.val();
            input_endate.datetimepicker('minDate', start_date);
            input_endate.datetimepicker('date', start_date);
            pnlEndDate.hide();
            if (id === 2) {
                pnlEndDate.show();
            }
        });

    /* Events Products */

    $('#btnRemoveProductsAll').on('click', function () {
        if (items.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los productos de tu detalle?', function () {
            items.details.products = [];
            items.list_products();
        });
    });

    $("#search_product").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_product',
                    'term': request.term,
                    'products': JSON.stringify(items.get_products_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.cant = 1;
            ui.item.state = true;
            items.add_products(ui.item);
            $(this).val('').focus();
        }
    });

    $('#clearSearchProduct').on('click', function () {
        $('#search_product').val('').focus();
    });

    $('#tblProducts tbody')
        .on('change', 'input[name="cant"]', function () {
            var td = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(td.row).data();
            items.details.products[row.pos].cant = $(this).val();
            items.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = items.details.products[row.pos].subtotal.toFixed(2);
            $('td:eq(5)', tr).html('$' + subtotal);
            $('span[name="total"]').html('$' + items.details.subtotal.toFixed(2));
        })
        /*.on('change', 'input[name="cost"]', function () {
            var td = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(td.row).data();
            items.details.products[row.pos].cost = parseFloat($(this).val());
            items.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = items.details.products[row.pos].subtotal.toFixed(2);
            $('td:eq(5)', tr).html('$' + subtotal);
            $('span[name="total"]').html('$' + items.details.subtotal.toFixed(2));
        })*/
        .on('click', 'a[rel="remove"]', function () {
            var td = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(td.row).data();
            items.details.products.splice(row.pos, 1);
            items.list_products();
        });

    /* Provider New */

    $("#search_prov").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    action: 'search_prov',
                    term: request.term,
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).val(ui.item.name);
            $(this).blur();
            prov = ui.item;
            $('#pruc').val(ui.item.ruc);
        }
    });

    $('#clearSearchProv').on('click', function () {
        prov = null;
        $('#pruc').val('');
        $('#search_prov').val('').focus();
    });

    $('#btnAddProv').on('click', function () {
        $('#myModalAddProv').modal('show');
    });

    $('#myModalAddProv').on('hidden.bs.modal', function () {
        fvProvider.resetForm(true);
    });

    $('[name="mobile"]').intlTelInput({
        utilsScript: '/static/lib/intl-tel-input-11.1.2/js/utils.js',
        autoPlaceholder: true,
        initialCountry: 'ec',
        onlyCountries: ["ec"],
        formatOnDisplay: false,
        allowDropdown: false
    });

    $('#id_ruc,#id_phone').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    /* Form Ingress */

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    input_datejoined.on('change.datetimepicker', function (e) {
        fvIngress.revalidateField('date_joined');
        input_endate.datetimepicker('minDate', e.date);
        input_endate.datetimepicker('date', e.date);
    });

    input_endate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        minDate: defaultDate
    });

    input_endate.datetimepicker('date', input_endate.val());

    input_endate.on('change.datetimepicker', function (e) {
        fvIngress.revalidateField('end_date');
    });

    pnlEndDate.hide();
});