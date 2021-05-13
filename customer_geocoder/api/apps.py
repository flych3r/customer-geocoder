from django.apps import AppConfig


class ApiConfig(AppConfig):
    """App configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_geocoder.api'
