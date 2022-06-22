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

    $('.btnAddBackup').on('click', function () {
        dialog_submit_to_ajax('Notificación',
            '¿Estas seguro de sacar un respaldo de la base de datos?',
            pathname,
            {
                'action': 'create',
            },
            function () {
                location.reload();
            })
    });

});
$(document).ready(function() {
    $('#data').attr('data-order', '[[0, "desc"]]');
} );