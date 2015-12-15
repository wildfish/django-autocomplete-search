from autocomplete_search import views

from . import models

class TestSearchModelA(views.SearchView):
    autocomplete_fields = {
        models.ModelA: ['name'],
    }
