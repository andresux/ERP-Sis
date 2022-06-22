var month,
    year,
    month_text,
    input_year,
    tblRolPay;

function search_rol() {
    year = input_year.val();
    month = $('select[name="month"]').val();
    month_text = $("#month option:selected").text();
    $('.btnDeleteSalary').prop('disabled', true);

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
                'action': 'search_rolpay',
                'year': year,
                'month': month
            },
            dataSrc: ""
        },
        columns: [
            {"data": "cont.emp.user.full_name"},
            {"data": "cont.job.name"},
            {"data": "cont.rmu"},
            {"data": "dayslab"},
            {"data": "cont.daysalary"},
            {"data": "rmu"},
            {"data": "ingress"},
            {"data": "egress"},
            {"data": "total"},
        ],
        columnDefs: [
            {
                targets: [-1, -4, -5, -7],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
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
            $('.btnDeleteSalary').prop('disabled', json.length === 0);
        },
    });
}

$(function () {

    tblRolPay = $('.table').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('select[name="month"]')
        .on('change.select2', function () {
            search_rol();
        });

    input_year = $('input[name="year"]');

    input_year.datetimepicker({
        locale: 'es',
        keepOpen: false,
        viewMode: 'years',
        format: 'YYYY'
    });

    input_year.datetimepicker('date', new moment().format('YYYY'));

    input_year.on('change.datetimepicker', function (e) {
        search_rol();
    });

    $('.btnDeleteSalary').on('click', function () {
        location.href = "/rrhh/salary/delete/" + year + "/" + month;
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
            // info: false,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_dsctos',
                    'type': type,
                    'id': rows.id,
                },
                dataSrc: ""
            },
            columns: [
                {"data": "element.name"},
                {"data": "element.calculation"},
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
});
