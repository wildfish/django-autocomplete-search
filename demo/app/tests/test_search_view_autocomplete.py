import string
from math import ceil
from urllib.parse import urlencode

from django.core.urlresolvers import reverse
from django_webtest import WebTestMixin
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text, builds, lists, tuples, just

from ..models import ModelA, ModelB


def string_containing(s, max_size=None, min_size=None, alphabet=None):
    part_max_size = (max_size - len(s)) // 2 if max_size else None
    part_min_size = ceil((min_size - len(s)) // 2) if min_size else None

    def _gen_str(pre, suf):
        return pre + s + suf

    return builds(_gen_str, text(min_size=part_min_size, max_size=part_max_size), text(min_size=part_min_size, max_size=part_max_size))


class SearchViewAutocomplete(WebTestMixin, TestCase):
    @given(
        text(min_size=1, max_size=255, alphabet=string.printable).filter(lambda s: s.strip()).flatmap(
            lambda s: tuples(
                just(s),
                lists(
                    tuples(
                        string_containing(s, max_size=255, alphabet=string.printable),
                        string_containing(s, max_size=255, alphabet=string.printable),
                    ),
                    max_size=10,
                )
            )
        )
    )
    def test_only_model_a_is_registered_with_the_view___only_autocomplete_results_for_model_a_are_returned(self, search_a_and_b_values):
        search, a_and_b_values = search_a_and_b_values

        for a, b in a_and_b_values:
            ModelA.objects.create(name=a)
            ModelB.objects.create(name=b)

        response = self.app.get(
            reverse('model_a_search') + '?autocomplete&' + urlencode({'q': search}),
        )

        expected_results = [{
            'app': 'app',
            'model': 'ModelA',
            'field': 'name',
            'q': a.name
        } for a in ModelA.objects.all()]

        self.assertListEqual(expected_results, response.json)
