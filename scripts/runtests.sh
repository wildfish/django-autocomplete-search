#!/usr/bin/env bash

cd demo

coverage run --source='autocomplete_search' --branch manage.py test
coverage report -m --fail-under=100
