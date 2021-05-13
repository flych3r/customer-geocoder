from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField()
    gender = models.CharField(max_length=256)
    company = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
