from django.db import models


class ModelA(models.Model):
    name = models.CharField(max_length=255)


class ModelB(models.Model):
    name = models.CharField(max_length=255)
