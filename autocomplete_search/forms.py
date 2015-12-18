import uuid

from django import forms
from django.apps import apps
from django.forms import widgets
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.template.loader import get_template
from haystack.forms import SearchForm
from haystack.inputs import Exact
from haystack.query import EmptySearchQuerySet


class AutocompleteSearchWidget(widgets.Input):
    def __init__(self, *args, url=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self._uuid = None

    @property
    def uuid(self):
        if not self._uuid:
            self._uuid = uuid.uuid4().hex
        return self._uuid

    def render(self, name, value, attrs=None):
        value = value or ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name, autocomplete='off')
        if value:
            final_attrs['value'] = force_text(self._format_value(value))

        return get_template('autocomplete_search/autocomplete_search_widget.html').render({
            'attrs': flatatt(final_attrs),
            'url': self.url,
            'uuid': self.uuid
        })


class AutocompleteSearchForm(SearchForm):
    q = forms.CharField(max_length=255, required=False, widget=AutocompleteSearchWidget)
    app = forms.CharField(max_length=255, required=False, widget=widgets.HiddenInput)
    model = forms.CharField(max_length=255, required=False, widget=widgets.HiddenInput)
    field = forms.CharField(max_length=255, required=False, widget=widgets.HiddenInput)

    def __init__(self, *args, url=None, **kwargs):
        super().__init__(*args, **kwargs)

        if not url:
            raise ValueError('"url" must be set')

        self.fields['q'].widget.url = url

    def search(self):
        # If the user has supplied a model and field to the query we only search for those specific results
        # If not we do a simple text search on the
        if self.cleaned_data['app'] and self.cleaned_data['model'] and self.cleaned_data['field']:
            try:
                model = apps.get_model(self.cleaned_data['app'], self.cleaned_data['model'])

                # haystack search with exact does not exact match the query, instead it makes sure the exact string
                # (including spaces) is in the field so Exact('q string') would match 'q string' and 'a q string b'.
                # Since we only want the results for exact matches we first get the ids for the objects we are
                # interested in and search on those,
                ids = model.objects.filter(**{self.cleaned_data['field']: self.cleaned_data['q']}).values_list('id', flat=True)
                if ids:
                    sqs = self.searchqueryset.filter(id__in=ids).models(model)
                else:
                    return EmptySearchQuerySet()
            except LookupError:
                return EmptySearchQuerySet()
        else:
            sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
