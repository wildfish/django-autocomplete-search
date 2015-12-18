import string
from itertools import chain
from urllib.parse import urlencode

from django.core.management import call_command
from django.core.urlresolvers import reverse
from django_webtest import WebTestMixin
from haystack.generic_views import RESULTS_PER_PAGE
from haystack.query import SearchQuerySet
from hypothesis import given, Settings
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text, just, tuples, lists
from ..models import ModelA, ModelC
from .strategies import string_containing, string_not_containing


class SearchViewResults(WebTestMixin, TestCase):
    @given(lists(text(min_size=1, max_size=255, alphabet=string.ascii_letters), max_size=50))
    def test_no_query_is_supplied___context_has_all_results(self, names):
        ModelA.objects.bulk_create(ModelA(name=n) for n in names)
        call_command('update_index', remove=True, verbosity=0)

        response = self.app.get(
            reverse('model_a_search'),
        )

        self.assertListEqual(
            list((r.pk, r.app_label, r.model_name) for r in SearchQuerySet()[:RESULTS_PER_PAGE]),
            list((r.pk, r.app_label, r.model_name) for r in response.context['object_list'])
        )

    @given(text(max_size=200, min_size=1, alphabet=string.ascii_letters).filter(lambda s: s.strip()).flatmap(lambda s: tuples(
            just(s),
            lists(string_containing(s, max_size=255, alphabet=string.ascii_letters, with_spacing=True), min_size=1, max_size=20),
            lists(string_not_containing(s, max_size=255, alphabet=string.ascii_letters), min_size=1, max_size=20),
        ))
    )
    def test_user_supplies_query_contained_by_some_objects___result_is_from_haystacks_normal_query(self, query_matching_missing):
        q, matching, missing = query_matching_missing

        ModelA.objects.bulk_create(ModelA(name=n) for n in chain(matching, missing))
        call_command('update_index', remove=True, verbosity=0)

        response = self.app.get(
            reverse('model_a_search') + '?' + urlencode({'q': q}),
        )

        self.assertListEqual(
            list((r.pk, r.app_label, r.model_name) for r in SearchQuerySet().auto_query(q)[:RESULTS_PER_PAGE]),
            list((r.pk, r.app_label, r.model_name) for r in response.context['object_list'])
        )

    @given(text(max_size=200, min_size=1, alphabet=string.ascii_letters).filter(lambda s: s.strip()).flatmap(lambda s: tuples(
            just(s),
            lists(
                tuples(
                    just(s),
                    string_not_containing(s, max_size=255, alphabet=string.ascii_letters),
                ),
                min_size=1,
                max_size=20
            ),
            lists(
                tuples(
                    string_containing(s, min_size=len(s) + 2, max_size=255, alphabet=string.ascii_letters),
                    just(s),
                ),
                min_size=1,
                max_size=20
            ),
        ))
    )
    def test_user_supplies_query_and_field_info_matched_by_some_objects___results_exactly_matching_the_model_and_field_are_returned(self, query_matching_missing):
        q, matching, missing = query_matching_missing

        ModelC.objects.bulk_create(ModelC(field_a=a, field_b=b) for a, b in chain(matching, missing))
        call_command('update_index', remove=True, verbosity=0)

        response = self.app.get(
            reverse('model_c_search') + '?' + urlencode({'app': 'app', 'model': 'ModelC', 'field': 'field_a', 'q': q}),
        )

        self.assertSetEqual(
            set(ModelC.objects.filter(field_a=q)),
            set(r.object for r in response.context['object_list'])
        )

    @given(text(max_size=200, min_size=1, alphabet=string.ascii_letters).filter(lambda s: s.strip()).flatmap(lambda s: tuples(
            just(s),
            lists(
                tuples(
                    string_containing(s, min_size=len(s) + 2, max_size=255, alphabet=string.ascii_letters),
                    string_containing(s, min_size=len(s) + 2, max_size=255, alphabet=string.ascii_letters),
                ),
                min_size=1,
                max_size=20
            ),
        ))
    )
    def test_user_supplies_query_and_field_info_matched_by_no_objects___no_results_are_returned(self, query_values):
        q, values = query_values

        ModelC.objects.bulk_create(ModelC(field_a=a, field_b=b) for a, b in values)
        call_command('update_index', remove=True, verbosity=0)

        response = self.app.get(
            reverse('model_c_search') + '?' + urlencode({'app': 'app', 'model': 'ModelC', 'field': 'field_a', 'q': q}),
        )

        self.assertEqual(0, len(response.context['object_list']))

    @given(text(max_size=200, min_size=1, alphabet=string.ascii_letters).filter(lambda s: s.strip()).flatmap(lambda s: tuples(
            just(s),
            string_containing(s, max_size=255, alphabet=string.ascii_letters, with_spacing=True),
        ))
    )
    def test_user_supplies_query_with_a_bad_model___no_results_are_returned(self, q_names):
        q, names = q_names

        ModelA.objects.bulk_create(ModelA(name=n) for n in names)
        call_command('update_index', remove=True, verbosity=0)

        response = self.app.get(
            reverse('model_a_search') + '?' + urlencode({'app': 'app', 'model': 'bad_model', 'field': 'field_a', 'q': q}),
        )

        self.assertEqual(0, len(response.context['object_list']))

    @given(text(max_size=200, min_size=1, alphabet=string.ascii_letters).filter(lambda s: s.strip()).flatmap(lambda s: tuples(
            just(s),
            string_containing(s, max_size=255, alphabet=string.ascii_letters, with_spacing=True),
        ))
    )
    def test_user_supplies_query_with_a_bad_app___no_results_are_returned(self, q_names):
        q, names = q_names

        ModelA.objects.bulk_create(ModelA(name=n) for n in names)
        call_command('update_index', remove=True, verbosity=0)

        response = self.app.get(
            reverse('model_a_search') + '?' + urlencode({'app': 'bad_app', 'model': 'ModelC', 'field': 'field_a', 'q': q}),
        )

        self.assertEqual(0, len(response.context['object_list']))

    @given(text(max_size=5, min_size=1, alphabet=string.ascii_letters).filter(lambda s: s.strip()).flatmap(lambda s: tuples(
            just(s),
            lists(string_containing(s, min_size=10, max_size=255, alphabet=string.ascii_letters, with_spacing=True), min_size=10, max_size=50),
        )),
        settings=Settings(max_examples=1),
    )
    def test_load_all_is_set___result_objects_are_loaded(self, q_names):
        q, names = q_names

        ModelA.objects.bulk_create(ModelA(name=n) for n in names)
        call_command('update_index', remove=True, verbosity=0)

        response = self.app.get(
            reverse('model_a_load_all_search') + '?' + urlencode({'q': q}),
        )

        self.assertGreater(len(response.context['object_list']), 0)
        self.assertTrue(all(o.object for o in response.context['object_list']))
