from django.db import models


class Customer(models.Model):
    """
    Db model for Customer.

    Parameters
    ----------
        first_name: str
            max 256 characters
        last_name: str
            max 256 characters
        email: str
            follows email validation
        gender: str
            max 256 characters
        company: str
            max 256 characters
        city: str
            max 256 characters
        title: str
            max 256 characters
        latitude: float
            between -90 and 90
        longitude: float
            between -180 and 180
    """

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField()
    gender = models.CharField(max_length=256)
    company = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    latitude = models.FloatField(min_value=-90, max_value=90)
    longitude = models.FloatField(min_value=-180.0, max_value=180.0)

    def __str__(self):
        """Model name."""
        return self.name
