$(function () {
    $('.btnDeleteAll').on('click', function () {
        dialog_submit_to_ajax('Notificación',
            '¿Estas seguro de eliminar todos los registros?',
            pathname,
            {
                'action': 'delete_access_all',
            },
            function () {
                location.reload();
            })
    });
});