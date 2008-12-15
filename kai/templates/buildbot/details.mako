<%!
from datetime import datetime
%>
<div class="close"><a href="#">${_('Close Window')}</a></div>
<div id="build-details" style="cursor: default">
    <h2>${_('Build Steps')}</h2>
    <table>
        <thead>
            <tr>
                <th>Step</th>
                <th>Start</th>
                <th>End</th>
            </tr>
        </thead>
        <tbody>
        % for step in c.details['steps']:
        <%
            pretty_text = ' '.join(step['text'])
            start = datetime.fromtimestamp(step['start'])
            end = datetime.fromtimestamp(step['end'])
        %>
        % if step['text'] and step['text'][-1] == 'failed':
            <tr class="build-step failure">
                <td>${pretty_text}</td>
                <td class="times">${format.datetime(start)}</td>
                <td class="times">${format.datetime(end)}</td>
            </tr>
            <tr><td colspan="3">
                <pre><code>
                ${'\n' + c.details['full_error'][step['name']]}
                </code></pre>
                </td>
            </tr>
            % else:
            <tr class="build-step success">
                <td class="success">${pretty_text}</td>
                <td class="times">${format.datetime(start)}</td>
                <td class="times">${format.datetime(end)}</td>
            </tr>
            % endif
            % endfor
        </tbody>
    </table>
</div>
<div class="close"><a href="#">${_('Close Window')}</a></div>
