var select_month,
    select_contracts,
    input_year;


function generate_report() {
    var parameters = {};
    parameters['action'] = 'search_report';
    parameters['year'] = input_year.val();
    parameters['month'] = select_month.val();
    parameters['contract'] = select_contracts.val();
    tblReport = $('#tblReport').DataTable({
        destroy: true,
        responsive: true,
        autoWidth: false,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ''
        },
        order: [[0, 'asc']],
        paging: false,
        ordering: true,
        // info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat'
            },
            {
                extend: 'pdfHtml5',
                text: 'Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ["15%", "10%", "10%", "10%", "10%", "10%", "10%", "10%", "15%"];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_joined}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        columnDefs: [
            {
                targets: ['_all'],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            }
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        },
    });
}

$(function () {

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });
    select_contracts = $('select[name="contracts"]');

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
        generate_report();
    });

    select_month.on('change', function () {
        generate_report();
    });

    select_contracts.on('change', function () {
        generate_report();
    });
});