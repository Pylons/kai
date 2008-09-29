$(document).ready(function() {
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
});
