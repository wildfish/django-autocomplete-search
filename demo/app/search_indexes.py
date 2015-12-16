from haystack import indexes
from .models import ModelA, ModelB, ModelC


class AIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return ModelA


class BIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return ModelB


class CIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    field_a = indexes.CharField(model_attr='field_a')
    field_b = indexes.CharField(model_attr='field_b')

    def get_model(self):
        return ModelC
