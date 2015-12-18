django-autocomplete-search
==========================

django-autocomplete-search enables you to create a site wide search that will autocomplete based off specified models
and fields. If no option from the autocomplete list is selected a normal text search will be performed. If one of the
autocomplete suggestions is selected the objects for the model that have the exact matching field will be returned.

Install
=======

Currently we don't have a proper bundle for this so to install it check out the project and from the project root run::

    $> nvm install
    $> npm install
    $> npm run build
    $> python setup.py install

.. _django-haystack: http://haystacksearch.org/
.. _docs: http://django-haystack.readthedocs.org/en/latest/
django-autocomplete-search runs on top of django-haystack_ so you will need to setup your
indexes according to their docs_. Additionally you will need to
install the python bindings for your chosen backend. For example if you are using elastic search you will need to run::

    $> pip install elasticsearch

Once you have the app installed into your environment you will need to add it to your ``INSALLED_APPS``::

    INSTALLED_APPS = (
        # django core apps
        
        'haystack',
        'autocomplete_search',
        
        # project apps
    )
    
And add the css and javascript into your template::

    <link href="{% static 'autocomplete_search/dist/autocomplete-search.css' %}" rel="stylesheet">
    <script src="{% static 'autocomplete_search/dist/autocomplete-search.js' %}"></script>

django 1.9
==========

Currently django-haystack does not support django 1.9 so this only supports 1.8 and lower. The latest development
version of django-haystack has fixed some issues with 1.9 so installing that may allow you to install this with
django 1.9.

Usage
=====

Using django-autocomplete-search is simple, just create a view inheriting from ``SearchView`` and supply a ``search_url``
and ``autocomplete_fields``::

    from django.core.urlresolvers import reverse_lazy
    from autocomplete_search import views
    
    from myapp import models
    
    
    class SearchModelA(views.SearchView):
        search_url = reverse_lazy('model_a_search')
        autocomplete_fields = {
            models.ModelA: ['name'],
        }

The ``search_url`` should be the url the view is registered to. This is the url used to fetch the autocomplete
suggestions from and the final search url.

The ``autocomplete_fields`` is used to specify the models and fields to use for suggestions. This is a dictionary of
model classes to an iterable of field names. In the above example sugestions will be created for ``ModelA`` based on
the field ``name``.

In addition the following fields can be set:

- ``template_name`` - The template to use to render the searhc results (default: ``search/indexes/search.html``)
- ``autocomplete_limit`` - The maximum number of suggestions to return, if None no limit is imposed (default: ``None``)
- ``lookup`` - The lookup to use for finding suggestions (default: ``icontains``)
- ``form_class`` - The class to use for runnung the search (default: ``AutocompleteSearchForm``)

To use a search form on a non search results page add a ``AutocompleteSearchForm`` instance to the context instantiated
with the required search url as the ``url`` parameter.
