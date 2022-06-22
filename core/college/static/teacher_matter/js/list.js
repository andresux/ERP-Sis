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
                {data: "course_mat.mat.name"},
                {data: "course_mat.course.classroom.name"},
                {data: "course_mat.course.level"},
                {data: "course_mat.course.period.name"},
            ],
            columnDefs: [
                {
                    targets: [0, -1, -2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
            ]
        });
        $('#myModalMatters').modal('show');
    });
});