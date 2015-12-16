from django.core.urlresolvers import reverse_lazy

from autocomplete_search import views

from . import models


class TestSearchModelA(views.SearchView):
    search_url = reverse_lazy('model_a_search')
    autocomplete_fields = {
        models.ModelA: ['name'],
    }


class TestSearchModelALoadAll(views.SearchView):
    search_url = reverse_lazy('model_a_load_all_search')
    autocomplete_fields = {
        models.ModelA: ['name'],
    }

    def get_form_kwargs(self):
        kwargs = super(TestSearchModelALoadAll, self).get_form_kwargs()
        kwargs['load_all'] = True
        return kwargs


class TestSearchModelALimit5(views.SearchView):
    search_url = reverse_lazy('model_a_limit_5_search')
    autocomplete_limit = 5
    autocomplete_fields = {
        models.ModelA: ['name'],
    }


class TestSearchModelCFieldA(views.SearchView):
    search_url = reverse_lazy('model_c_field_a_search')
    autocomplete_fields = {
        models.ModelC: ['field_a'],
    }


class TestSearchModelC(views.SearchView):
    search_url = reverse_lazy('model_c_search')
    autocomplete_fields = {
        models.ModelC: ['field_a', 'field_b'],
    }
