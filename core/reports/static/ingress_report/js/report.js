var start_date = null,
    end_date = null,
    month = null,
    filter = null,
    year = null,
    frm_search,
    select_month,
    input_year;


function parameters_report() {
    filter = $('#filter').val();
    month = select_month.val();
    year = input_year.val();
    start_date = start_date == null ? "" : start_date;
    end_date = end_date == null ? "" : end_date;

    if (month === "" && filter === '3') {
        filter = '2';
    }

    return {
        filter: filter,
        year: year,
        month: month,
        start_date: start_date,
        end_date: end_date,
        action: 'search_report'
    }
}

function generate_report() {
    var parameters = parameters_report();
    parameters['action'] = 'search_report';
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
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
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
                    doc.content[1].table.widths = ["5%", "15%", "15%","15%", "15%", "15%", "10%", "10%"];
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
                targets: [-1, -2, -3],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
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

    frm_search = document.getElementsByClassName('frm-search');
    $(frm_search).hide();
    start_date = moment().format("YYYY-MM-DD");
    end_date = moment().format("YYYY-MM-DD");

    $('#filter').change(function () {
        filter = $(this).val();
        $(frm_search).hide();
        if (tblReport != null) tblReport.clear().draw();
        if (filter) {
            switch (filter) {
                case '1':
                    $(frm_search[0]).show();
                    break;
                case '2':
                    $(frm_search[1]).show();
                    break;
                case '3':
                    $(frm_search[1]).show();
                    $(frm_search[2]).show();
                    break;
            }
            generate_report();
        }
    });

    $('#date_range')
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            start_date = picker.startDate.format('YYYY-MM-DD');
            end_date = picker.endDate.format('YYYY-MM-DD');
            generate_report();
        });

    select_month.on('change', function () {
        generate_report();
    });
});