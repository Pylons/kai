<%!
from kai.model.forms import snippet_form
%>
<h1>${_('Add Snippet')}</h1>
<p>${_("""Pylons snippet repository is a place to share their code snippets with the community.
    Please only share fully functioning and tested snippets and include instructions so
    that novice and experienced Pylons users can benefit.""")}</p>

${snippet_form.display(action=url('snippets')) | n}

<div style="display: none; border: 2px solid #444; padding: 4px;" id="snippet_preview">&nbsp;</div>

<%def name="title()">${parent.title()} - ${_('Add Snippet')}</%def>
<%def name="javascript()">
${parent.javascript()}
<script src="http://yui.yahooapis.com/2.6.0/build/yuiloader/yuiloader-min.js" ></script>
<script src="/javascripts/rst_helpers.js" charset="utf-8"></script>
<script>
$(document).ready(function() {
    var loader = new YAHOO.util.YUILoader({
        require: ["autocomplete"],
        loadOptional: true,
        onSuccess: function() {            
            make_tagger = function(tag_field, tag_box, datafield) {
                var data_source = new YAHOO.widget.DS_JSArray(datafield);
                var myAutoComp = new YAHOO.widget.AutoComplete(tag_field, tag_box, data_source);
                myAutoComp.typeAhead = true;
                myAutoComp.queryDelay = 0;
                myAutoComp.minQueryLength = 2;
                myAutoComp.delimChar = [" ", ","];
                return true;
            };
            var tags = [${','.join(["\"%s\"" % tag for tag in c.tags]) | n}];
            make_tagger('snippet_form_tags', 'snippet_form_tags_autocomplete', tags);
        }
    });
    loader.insert();
    $('#preview').click(function() {
        var content = $('#snippet_form_content')[0].value;
        var preview_url = '${url('preview_snippet')}';
        $.ajax({
            data: {content:content},
            type: "POST",
            url: preview_url,
            success: function(data, textStatus) {
                $('#snippet_preview').html(data).slideDown();
            }
        });
        return false;
    });
})
</script>
</%def>
<%inherit file="layout.mako" />