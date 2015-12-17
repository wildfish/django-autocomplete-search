import $ from 'jquery/dist/jquery';
import ui from 'jquery-ui/jquery-ui';

var _currentSearchRequest = null;

export default function init(selector, url) {
    var elem = $(selector);

    elem.autocomplete({
        source: function( request, response ) {
            // close down the current request if its firing
            if(_currentSearchRequest) {
                _currentSearchRequest.abort();
            }

            // make the new request
            _currentSearchRequest = $.get(url, {
                q: request.term,
                autocomplete: true
            }).done(response);
        },
        minLength: 2,
        select: function( event, ui ) {
            if(ui.item) {
                window.location = url + '?' + $.param(ui.item);
            }
        }
    })
}
