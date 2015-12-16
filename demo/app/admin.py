from django.contrib.admin import site

from .models import ModelA, ModelB, ModelC

site.register(ModelA)
site.register(ModelB)
site.register(ModelC)
