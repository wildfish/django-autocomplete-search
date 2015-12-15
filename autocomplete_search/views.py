from django.http import JsonResponse
from django.views.generic import TemplateView


class SearchView(TemplateView):
    autocomplete_fields = {}
    lookup = 'icontains'
    autocomplete_limit = None

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
                _lookup = self.get_field_lookup(model, field)

                for q in model.objects.filter(**{_lookup: self.request.GET['q']}).values_list(field, flat=True):
                    results.append({
                        'app': model._meta.app_label,
                        'model': model._meta.object_name,
                        'field': field,
                        'q': q
                    })

                if self.get_autocomplete_limit() and len(results) >= self.get_autocomplete_limit():
                    return JsonResponse(results[:self.get_autocomplete_limit()], safe=False)

        return JsonResponse(results, safe=False)

    def get(self, request, *args, **kwargs):
        if 'autocomplete' in request.GET:
            return self.get_autocomplete_results()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # perform actual search
        return super().get_context_data(**kwargs)