$(document).ready(function() {
    // Trigger the recent mail list thread loading
    var ml = $('#maillist');
    ml.html('Loading');
    var data = {mode:'json', page:1, q:'list:pylons'};
    var searchResults = $.getJSON('http://markmail.org/results.xqy?callback=?', data,
        function(data) {
            ml.html('');
            // If there's no search results, stop here
            if (!data.search.results) {
                return false;
            }
            
            // Iterate through the search results adding them dynamically
            // to the element
            $.each(data.search.results.result, function(i, val) {
                var result = $(document.createElement('div')).addClass('result');
                var link = document.createElement('a');
                link.href = 'http://markmail.org' + val.url.replace(/\?callback.*?\&/, '?');
                link.target = '_blank';
                $(link).html(val.subject);
                result.append(link);
                var blurb = $(document.createElement('div')).addClass('blurb');
                
                // Pull out just the first 50 words
                var words = val.blurb.split(' ', limit=25);
                blurb.html(words.join(' '));
                result.append(blurb);
                var meta = $(document.createElement('div')).addClass('meta');
                meta.html(val.date + ' - ' + val.from);
                result.append(meta);
                ml.append(result);
            });
            var searchlink = document.createElement('a');
            searchlink.href = data.search.permalink;
            searchlink.target = '_blank';
            $(searchlink).html('View entire mail list');
            var numresults = $(document.createElement('p'));
            numresults.addClass('results');
            numresults.prepend(searchlink);            
            ml.append(numresults);
        }
    );
    
});
