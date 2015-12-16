from unittest import TestCase

from autocomplete_search.forms import AutocompleteSearchForm


class AutocompleteSearchFormInit(TestCase):
    def test_url_is_not_supplied___value_error_is_raised(self):
        self.assertRaisesRegex(ValueError, '"url" must be supplied', AutocompleteSearchForm)
