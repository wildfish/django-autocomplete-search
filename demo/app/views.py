from autocomplete_search import views

from . import models


class TestSearchModelA(views.SearchView):
    autocomplete_fields = {
        models.ModelA: ['name'],
    }


class TestSearchModelALimit5(views.SearchView):
    autocomplete_limit = 5
    autocomplete_fields = {
        models.ModelA: ['name'],
    }


class TestSearchModelCFieldA(views.SearchView):
    autocomplete_fields = {
        models.ModelC: ['field_a'],
    }


class TestSearchModelC(views.SearchView):
    autocomplete_fields = {
        models.ModelC: ['field_a', 'field_b'],
    }
