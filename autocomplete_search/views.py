from django.http import JsonResponse
from haystack.generic_views import SearchView as HaystackSearchView
from haystack.query import SearchQuerySet

from .forms import AutocompleteSearchForm


class SearchView(HaystackSearchView):
    autocomplete_fields = {}
    lookup = 'icontains'
    autocomplete_limit = None
    search_url = None
    form_class = AutocompleteSearchForm

    def get_queryset(self):
        return SearchQuerySet()

    def get_form_kwargs(self):
        kwargs = super(SearchView, self).get_form_kwargs()
        kwargs['url'] = self.get_search_url()
        return kwargs

    def get_search_url(self):
        return self.search_url

    def get_autocomplete_limit(self):
        return self.autocomplete_limit

    def get_autocomplete_fields(self):
        return self.autocomplete_fields

    def get_field_lookup(self, model, field):
        return '{}__{}'.format(field, self.lookup)

    def get_autocomplete_results(self):
        results = []

        for model, fields in self.get_autocomplete_fields().items():
            for field in fields:
                queryset = self.get_queryset().models(model).autocomplete(**{field: self.request.GET['q']})
                objects = [r.object for r in queryset if r.object]
                for q in set(getattr(o, field) for o in objects):
                    results.append({
                        'app': model._meta.app_label,
                        'model': model._meta.object_name,
                        'field': field,
                        'q': q,
                        'label': q
                    })

        return JsonResponse(sorted(results, key=lambda x: self.autocomplete_ordering(x))[:self.get_autocomplete_limit()], safe=False)

    def autocomplete_ordering(self, elem):
        return elem['q'].lower(), elem['field'].lower(), elem['model'].lower(), elem['app'].lower()

    def get(self, request, *args, **kwargs):
        if 'autocomplete' in request.GET:
            return self.get_autocomplete_results()

        return super().get(request, *args, **kwargs)
