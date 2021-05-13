from rest_framework import serializers

from customer_geocoder.api.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """API serializer for Customer model."""

    class Meta:
        model = Customer
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'company',
            'city',
            'title',
            'latitude',
            'longitude'
        )
