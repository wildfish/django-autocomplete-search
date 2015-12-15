from django.db import models


class ModelA(models.Model):
    name = models.CharField(max_length=255)


class ModelB(models.Model):
    name = models.CharField(max_length=255)


class ModelC(models.Model):
    field_a = models.CharField(max_length=255)
    field_b = models.CharField(max_length=255)
