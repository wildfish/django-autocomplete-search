import string

from django.forms.utils import flatatt
from django.template.loader import get_template
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text, dictionaries

from autocomplete_search.forms import AutocompleteSearchWidget
from .strategies import false_values


class AutocompleteSearchWidgetRender(TestCase):
    @given(
        text(min_size=1, max_size=50, alphabet=string.ascii_letters),
        text(min_size=1, max_size=50, alphabet=string.ascii_letters),
        dictionaries(text(min_size=1, max_size=50, alphabet=string.ascii_letters).filter(lambda s: s != 'name'), text(min_size=1, max_size=50, alphabet=string.ascii_letters), max_size=10),
        false_values(),
    )
    def test_value_is_false___result_is_rendered_without_the_value(self, url, name, attrs, value):
        widget = AutocompleteSearchWidget(url=url)
        render = widget.render(name, value, attrs)

        attrs['name'] = name
        attrs['type'] = None
        expected_render = get_template('autocomplete_search/autocomplete_search_widget.html').render({
            'url': url,
            'attrs': flatatt(attrs),
            'uuid': widget.uuid
        })

        self.assertHTMLEqual(expected_render, render)

    @given(
        text(min_size=1, max_size=50, alphabet=string.ascii_letters),
        text(min_size=1, max_size=50, alphabet=string.ascii_letters),
        dictionaries(text(min_size=1, max_size=50, alphabet=string.ascii_letters).filter(lambda s: s != 'name'), text(min_size=1, max_size=50, alphabet=string.ascii_letters), max_size=10),
        text(min_size=1, max_size=50, alphabet=string.ascii_letters),
    )
    def test_value_is_not___result_is_rendered_with_the_value(self, url, name, attrs, value):
        widget = AutocompleteSearchWidget(url=url)
        render = widget.render(name, value, attrs)

        attrs['name'] = name
        attrs['type'] = None
        attrs['value'] = value
        expected_render = get_template('autocomplete_search/autocomplete_search_widget.html').render({
            'url': url,
            'attrs': flatatt(attrs),
            'uuid': widget.uuid
        })

        self.assertHTMLEqual(expected_render, render)
