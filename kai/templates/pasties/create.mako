<%!
from kai.model.forms import pastebin_form
%>
<h1>${_('Create Paste')}</h1>

${pastebin_form() | n}

<%def name="title()">${parent.title()} - ${_('Create Paste')}</%def>
<%def name="javascript()">
${parent.javascript()}
<script src="http://yui.yahooapis.com/2.6.0/build/yuiloader/yuiloader-min.js" ></script>
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
            make_tagger('pastebin_form_tags', 'pastebin_form_tags_autocomplete', tags);
        }
    });
    loader.insert();
})
</script>
</%def>
<%inherit file="layout.mako" />