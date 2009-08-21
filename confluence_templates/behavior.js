$(document).ready(function() {
    // Swap the layout toggle if they have wide-screen
    if ($.cookie('layout_style') == 'Stretch') {
        $('#doc4').attr('id', 'doc3');
        $('#layout-toggle').html('Stretch');
    };
    $('#layout-toggle').click(function() {
        if ($('#layout-toggle').html() == 'Fixed-width') {
            $('#doc4').attr('id', 'doc3');
            $('#layout-toggle').html('Stretch');
            $.cookie('layout_style', 'Stretch', {path: '/', domain: 'pylonshq.com'});
        } else {
            $('#doc3').attr('id', 'doc4');
            $('#layout-toggle').html('Fixed-width');
            $.cookie('layout_style', null, {path: '/', domain: 'pylonshq.com'});
        }
        return false;
    });
});
