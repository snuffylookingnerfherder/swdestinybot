from django.db import models

class Card(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    search = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200, null=True)