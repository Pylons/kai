<%!
    from kai.model.forms import new_article_form
%>
<div class="yui-b content">
    <p>${h.link_to('< Back to all blog entries', url=url('articles'))}</p>
    <h1>${_('Add new blog posting')}</h1>
    <div style="display: none;" id="comment_preview">&nbsp;</div>
    ${new_article_form.display(action=url('articles')) | n}
</div>
<%def name="title()">${parent.title()} - ${'Blog'} - ${c.article.title}</%def>
<%inherit file="/layout.mako" />
<%def name="javascript()">
${parent.javascript()}
<script>
$(document).ready(function() {
    $('#Preview').click(function() {
        var content = $('#body')[0].value;
        var preview_url = '${url('preview_comment')}';
        $.ajax({
            data: {content:content},
            type: "POST",
            url: preview_url,
            success: function(data, textStatus) {
                $('#comment_preview').html(data).slideDown();
            }
        });
        return false;
    });
});
</script>
</%def>