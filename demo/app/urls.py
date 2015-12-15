from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^model-a-search/$', views.TestSearchModelA.as_view(), name='model_a_search'),
    url(r'^model-a-limit-5-search/$', views.TestSearchModelALimit5.as_view(), name='model_a_limit_5_search'),
    url(r'^model-c-field-a-search/$', views.TestSearchModelCFieldA.as_view(), name='model_c_field_a_search'),
    url(r'^model-c-search/$', views.TestSearchModelC.as_view(), name='model_c_search'),
]
