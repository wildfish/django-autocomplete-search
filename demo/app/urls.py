from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^model-a-search/$', views.TestSearchModelA.as_view(), name='model_a_search')
]