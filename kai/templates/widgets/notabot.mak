<%!
from webhelpers.rails.urls import js_obfuscate
%>
${js_obfuscate('<input type="hidden" name="notabot" value="%s" />' % value) | n}