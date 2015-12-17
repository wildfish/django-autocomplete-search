from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from autocomplete_search.forms import AutocompleteSearchForm


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('model_a_form', AutocompleteSearchForm(url=reverse('model_a_search')))
        kwargs.setdefault('model_a_limit_5_form', AutocompleteSearchForm(url=reverse('model_a_limit_5_search')))
        kwargs.setdefault('model_a_load_all_form', AutocompleteSearchForm(url=reverse('model_a_load_all_search')))
        kwargs.setdefault('model_c_field_a_form', AutocompleteSearchForm(url=reverse('model_c_field_a_search')))
        kwargs.setdefault('model_c_form', AutocompleteSearchForm(url=reverse('model_c_search')))
        return super(Home, self).get_context_data(**kwargs)
