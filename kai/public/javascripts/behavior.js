$(document).ready(function() {
    // Swap the layout toggle if they have wide-screen
    if ($.cookie('layout_style') == 'Stretch') {
        $('#doc4').attr('id', 'doc3');
        $('#layout-toggle').html('Stretch');
    };
    
    $('div.viewtoggle a').click(function() {
        $(this).toggleClass('down');
        $(this).parent().next().slideToggle();
        return false;
    });
    $('div.details a').click(function() {
        $.blockUI({ message: $('#buildinfo') });
        var url = '/buildbot/details/' + $(this).attr('class');
        $.ajax({
            url: url,
            cache: false,
            success: function(data, textStatus) {
                $.blockUI({ message: data, 
                            css: { width: '90%', top: '5%', 
                                   bottom: '5%', left: '5%',
                                   overflow: 'auto', right: '5%',
                                   textAlign: 'left', cursor: 'default' } });
                $('div.close a').click(function() {
                    $.unblockUI();
                    return false;
                });
            }
        });
        return false;
    });
    $('#layout-toggle').click(function() {
        if ($('#layout-toggle').html() == 'Fixed-width') {
            $('#doc4').attr('id', 'doc3');
            $('#layout-toggle').html('Stretch');
            $.cookie('layout_style', 'Stretch', {path: '/', domain: '.pylonshq.com'});
        } else {
            $('#doc3').attr('id', 'doc4');
            $('#layout-toggle').html('Fixed-width');
            $.cookie('layout_style', null, {path: '/', domain: '.pylonshq.com'});
        }
        return false;
    });
});
