<%!
from kai.model.forms import snippet_form
%>
<h1>${_('Edit Snippet')}</h1>

${snippet_form(dict(title=c.snippet.title, description=c.snippet.description,
                    content=c.snippet.content, tags=', '.join(c.snippet.tags or [])
               ), action=url('snippet', id=c.id, _method='PUT')) | n}

<div style="display: none; border: 2px solid #444; padding: 4px;" id="snippet_preview">&nbsp;</div>

<%def name="title()">${parent.title()} - ${_('Edit Snippet')}</%def>
<%def name="javascript()">
${parent.javascript()}
<script src="http://yui.yahooapis.com/2.6.0/build/yuiloader/yuiloader-min.js" ></script>
<script>
function getCaretPosition(element){
  var caret = 0;
  if ('selectionStart' in element) {  // W3
    var selectionStart = element.selectionStart;
    var selectionEnd = element.selectionEnd;
    return selectionStart;
  } else {  // IE
    // Walk up the tree looking for this textarea's document node.
    var doc = element;
    while (doc.parentNode) {
      doc = doc.parentNode;
    }
    if (!doc.selection || !doc.selection.createRange) {
      // Not IE?
      return null;
    }
    var range = doc.selection.createRange();
    if (range.parentElement() != element) {
      // Cursor not in this textarea.
      return null;
    }
    var newRange = doc.body.createTextRange();

    var collapsed = (range.text == '');
    newRange.moveToElementText(element);
    if (!collapsed) {
      newRange.setEndPoint('EndToEnd', range);
    }
    newRange.setEndPoint('EndToStart', range);
    var startPrefix = newRange.text;
    return startPrefix.length;
  }
}
/* 
http://stackoverflow.com/questions/29709/how-do-i-get-the-coordinates-of-the-caret-in-text-boxes
*/

function insertAtCaret(myField, myValue) {
    
    /* selecion model - ie */
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
    }
    
    /* field.selectionstart/end  firefox */ 
    else if (myField.selectionStart || myField.selectionStart == '0' ) {
        
        var startPos = myField.selectionStart;
        var endPos = myField.selectionEnd;
        myField.value = myField.value.substring(0, startPos)
            + myValue
            + myField.value.substring(endPos, myField.value.length);
        
        myField.selectionStart = startPos + myValue.length;
        myField.selectionEnd = startPos + myValue.length;
        myField.focus();
        } 
        
        // cursor not active/present
    else {
        myField.value += myValue;
    }
}
var contentbox = document.getElementById("snippet_form_content");
contentbox.focus();
if(contentbox.addEventListener ) {
    contentbox.addEventListener('keydown',this.keyHandler,false);
} else if(contentbox.attachEvent ) {
    contentbox.attachEvent('onkeydown',this.keyHandler); /* damn IE hack */
}

var onchange_timer = null;
function keyHandler(e) {
    var TABKEY = 9;
    if(e.keyCode == TABKEY) {
        setTimeout(function(){
            var sc = contentbox.scrollTop;
            var caret = getCaretPosition(contentbox);
            var val = contentbox.value.substr(0, caret);
            var i = val.lastIndexOf('\n');
            var v = '    ';
            switch((val.length - i - 1) % 4){
            case 1:
                v = '   ';
                break;
            case 2:
                v = '  ';
                break;
            case 3:
                v = ' ';
                break;
            }
            insertAtCaret(contentbox, v);
            contentbox.scrollTop = sc;
        },0)
        if(e.preventDefault) {
            e.preventDefault();
        }
        return false;
    }
}

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
    $('input#snippet_form_preview').click(function() {
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