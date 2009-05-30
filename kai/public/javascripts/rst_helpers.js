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
    var ENTER = 13;
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
    } else if (e.keyCode == ENTER) {
        setTimeout(function(){
            var sc = contentbox.scrollTop;
            var caret = getCaretPosition(contentbox);
            var val = contentbox.value.substr(0, caret);
            var i = val.lastIndexOf('\n');
            if (i > 0 && i+1 < caret) {
                var curline = contentbox.value.substring(i+1, caret);
                var spaces = curline.replace(/^(\s+).*/, '$1');
                var v = '';
                if (spaces.match(/^\s+$/)) {
                    v = '\n' + spaces;
                } else {
                    v = '\n';
                }
                insertAtCaret(contentbox, v);
                contentbox.scrollTop = sc;
            } else {
                insertAtCaret(contentbox, '\n');
                contentbox.scrollTop = sc;
            }
        },0)
        if(e.preventDefault) {
            e.preventDefault();
        }        
    }
}
