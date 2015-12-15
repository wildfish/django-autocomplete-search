from django import forms
from django.forms import widgets
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.template.loader import get_template
from haystack.forms import SearchForm


class AutocompleteSearchWidget(widgets.Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = None

    def render(self, name, value, attrs=None):
        value = value or ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value:
            final_attrs['value'] = force_text(self._format_value(value))

        return get_template('autocomplete_search_widget.html').render({
            'attrs': flatatt(final_attrs),
            'url': self.url,
        })


class AutocompleteSearchForm(SearchForm):
    q = forms.CharField(max_length=255, widget=AutocompleteSearchWidget)
    app = forms.CharField(max_length=255, required=False)
    model = forms.CharField(max_length=255, required=False)
    field = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, url=None, **kwargs):
        super().__init__(*args, **kwargs)

        if not url:
            raise ValueError('"url" must be set')

        self.fields['q'].widget.url = url
