$(function () {
    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var td = table.cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data();
        var id = parseInt(rows[0]);
        $('#tblCompDetails').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    action: 'search_details', id: id
                },
                dataSrc: ""
            },
            columns: [
                {data: "prod.name"},
                {data: "prod.cat.name"},
                {data: "price"},
                {data: "cant"},
                {data: "total"},
            ],
            columnDefs: [
                {
                    targets: [-1, -3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<b>'+data+'</b>';
                    }
                }
            ]
        });
        $('#myModalInventory').modal('show');
    });
});
