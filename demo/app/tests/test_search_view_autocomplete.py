import string
from math import ceil
from urllib.parse import urlencode

from django.core.urlresolvers import reverse
from django_webtest import WebTestMixin
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text, builds, lists, tuples, just

from ..models import ModelA, ModelB, ModelC


def string_containing(s, max_size=None, min_size=None, alphabet=None):
    part_max_size = (max_size - len(s)) // 2 if max_size else None
    part_min_size = ceil((min_size - len(s)) // 2) if min_size else None

    def _gen_str(pre, suf):
        return pre + s + suf

    return builds(_gen_str, text(min_size=part_min_size, max_size=part_max_size, alphabet=alphabet), text(min_size=part_min_size, max_size=part_max_size, alphabet=alphabet))


def string_not_containing(s, max_size=None, min_size=None, alphabet=None, average_size=None):
    return text(min_size=max_size, max_size=min_size, average_size=average_size, alphabet=alphabet).filter(lambda _s: s.lower() not in _s.lower())


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
                    min_size=1,
                )
            )
        )
    )
    def test_only_model_a_is_registered_with_the_view___only_autocomplete_results_for_model_a_are_returned(self, search_a_and_b_values):
        search, a_and_b_values = search_a_and_b_values
        a_values, b_values = zip(*a_and_b_values)

        ModelA.objects.bulk_create(ModelA(name=a) for a in set(a_values))
        ModelB.objects.bulk_create(ModelB(name=b) for b in set(b_values))

        response = self.app.get(
            reverse('model_a_search') + '?autocomplete&' + urlencode({'q': search}),
        )

        expected_results = [{
            'app': 'app',
            'model': 'ModelA',
            'field': 'name',
            'q': a,
        } for a in set(a_values)]

        expected_results = sorted(expected_results, key=lambda x: (x['q'].lower(), x['field'], x['model'], x['app']))

        self.assertListEqual(expected_results, response.json)

    @given(
        text(min_size=1, max_size=255, alphabet=string.printable).filter(lambda s: s.strip()).flatmap(
            lambda s: tuples(
                just(s),
                lists(
                    tuples(
                        string_not_containing(s, max_size=255, alphabet=string.printable),
                        string_containing(s, max_size=255, alphabet=string.printable),
                    ),
                    max_size=10,
                    min_size=1,
                )
            )
        )
    )
    def test_only_model_c_field_a_is_registered_with_the_view_only_field_b_has_the_search_string___no_results_are_returned(self, search_a_and_b_values):
        search, a_and_b_values = search_a_and_b_values

        ModelC.objects.bulk_create(ModelC(field_a=a, field_b=b) for a, b in a_and_b_values)

        response = self.app.get(
            reverse('model_c_field_a_search') + '?autocomplete&' + urlencode({'q': search}),
        )

        expected_results = []

        self.assertListEqual(expected_results, response.json)

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
                    min_size=1,
                )
            )
        )
    )
    def test_only_model_c_is_registered_with_the_view_both_fields_have_the_search_result___both_fields_have_entries_in_the_result(self, search_a_and_b_values):
        search, a_and_b_values = search_a_and_b_values

        ModelC.objects.bulk_create(ModelC(field_a=a, field_b=b) for a, b in a_and_b_values)

        response = self.app.get(
            reverse('model_c_search') + '?autocomplete&' + urlencode({'q': search}),
        )

        a_values, b_values = zip(*a_and_b_values)

        expected_results = [{
            'app': 'app',
            'model': 'ModelC',
            'field': 'field_a',
            'q': a,
        } for a in set(a_values)]

        expected_results.extend([{
            'app': 'app',
            'model': 'ModelC',
            'field': 'field_b',
            'q': b,
        } for b in set(b_values)])

        expected_results = sorted(expected_results, key=lambda x: (x['q'].lower(), x['field'], x['model'], x['app']))

        self.assertListEqual(expected_results, response.json)

    @given(
        text(min_size=1, max_size=255, alphabet=string.printable).filter(lambda s: s.strip()).flatmap(
            lambda s: tuples(
                just(s),
                lists(string_containing(s, max_size=255, alphabet=string.printable), max_size=10, unique=True)
            )
        )
    )
    def test_duplicate_values_exist___each_entry_only_appears_once(self, search_values):
        search, values = search_values

        ModelA.objects.bulk_create(ModelA(name=v) for v in values)
        ModelA.objects.bulk_create(ModelA(name=v) for v in values)

        response = self.app.get(
            reverse('model_a_search') + '?autocomplete&' + urlencode({'q': search}),
        )

        expected_results = [{
            'app': 'app',
            'model': 'ModelA',
            'field': 'name',
            'q': v,
        } for v in values]

        expected_results = sorted(expected_results, key=lambda x: (x['q'].lower(), x['field'], x['model'], x['app']))

        self.assertListEqual(expected_results, response.json)

    @given(
        text(min_size=1, max_size=255, alphabet=string.printable).filter(lambda s: s.strip()).flatmap(
            lambda s: tuples(
                just(s),
                lists(string_containing(s, max_size=255, alphabet=string.printable), max_size=10, unique=True)
            )
        )
    )
    def test_duplicate_values_exist___each_entry_only_appears_once(self, search_values):
        search, values = search_values

        ModelA.objects.bulk_create(ModelA(name=v) for v in values)
        ModelA.objects.bulk_create(ModelA(name=v) for v in values)

        response = self.app.get(
            reverse('model_a_search') + '?autocomplete&' + urlencode({'q': search}),
        )

        expected_results = [{
            'app': 'app',
            'model': 'ModelA',
            'field': 'name',
            'q': v,
        } for v in values]

        expected_results = sorted(expected_results, key=lambda x: (x['q'].lower(), x['field'], x['model'], x['app']))

        self.assertListEqual(expected_results, response.json)

    @given(
        text(min_size=1, max_size=200, alphabet=string.printable).filter(lambda s: s.strip()).flatmap(
            lambda s: tuples(
                just(s),
                lists(string_containing(s, max_size=255, alphabet=string.printable), min_size=5, max_size=20, unique=True)
            )
        )
    )
    def test_autocomplete_is_restricted_to_a_number_of_values___the_number_of_results_does_not_exceed_the_limit(self, search_values):
        search, values = search_values

        ModelA.objects.bulk_create(ModelA(name=v) for v in values)

        response = self.app.get(
            reverse('model_a_limit_5_search') + '?autocomplete&' + urlencode({'q': search}),
        )

        expected_results = [{
            'app': 'app',
            'model': 'ModelA',
            'field': 'name',
            'q': v,
        } for v in values]

        expected_results = sorted(expected_results, key=lambda x: (x['q'].lower(), x['field'], x['model'], x['app']))

        self.assertListEqual(expected_results[:5], response.json)
