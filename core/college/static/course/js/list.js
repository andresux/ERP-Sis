$(function () {
    $('#data tbody').on('click', 'a[rel="matters"]', function () {
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
                {data: "mat.name"},
            ],
            columnDefs: [
            ]
        });
        $('#myModalMatters').modal('show');
    });
});