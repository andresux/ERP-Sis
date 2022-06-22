function search(){
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'search',
                'date_joined': $('#date_joined').val(),
            },
            dataSrc: ""
        },
        columns: [
            {data: "id"},
            {data: "date_joined"},
            {data: "hour"},
            {data: "module"},
            {data: "action"},
            {data: "username"},
            {data: "username"},
        ],
        columnDefs: [
            {
                targets: [-1],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return  '<a href="/logs/audit/delete/'+row.id+'/" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                }
            },
        ],
    });

}

$(function () {

    $('.btnDeleteAll').on('click', function () {
        dialog_submit_to_ajax('Notificación',
            '¿Estas seguro de eliminar todos los registros?',
            pathname,
            {
                'action': 'delete_all',
            },
            function () {
                location.reload();
            });
    });

     $('input[name="date_joined"]').datetimepicker({
         format: 'YYYY-MM-DD',
         locale: 'es',
         defaultDate: new moment().format("YYYY-MM-DD")
     });
});