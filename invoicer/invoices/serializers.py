from django.core.validators import MinValueValidator
from rest_framework import serializers

from invoicer.invoices.models import Invoice
from invoicer.invoices.payment_types import payment_registry


class PaymentTypeSerializer(serializers.Serializer):
    label = serializers.CharField()
    is_enabled = serializers.BooleanField()
    domestic_url = serializers.CharField()


class InvoiceSerializer(serializers.ModelSerializer):
    payment_type = serializers.ChoiceField(required=True, choices=list(payment_registry.keys()))
    amount = serializers.DecimalField(max_digits=18, decimal_places=2, validators=(MinValueValidator(0.01),), required=True)

    class Meta:
        model = Invoice
        fields = ("amount", "payment_type", "description", "currency")
