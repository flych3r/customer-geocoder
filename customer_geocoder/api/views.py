from rest_framework import permissions, viewsets

from customer_geocoder.api.models import Customer
from customer_geocoder.api.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Customers to be viewed or edited."""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
