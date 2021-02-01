import pytest
from django.db import IntegrityError

from invoicer.invoices.models import Invoice, InvoiceCurrency


@pytest.mark.django_db
class TestInvoiceModel:
    @pytest.fixture
    def creation_data(self):
        return {
            "amount": 24.43,
            "description": "Описание платежа",
            "currency": InvoiceCurrency.ROUBLES,
            "payment_type": "paypal",
        }

    def test_invoice_creation(self, creation_data):
        test_invoice = Invoice.objects.create(**creation_data)
        for k, v in creation_data.items():
            assert getattr(test_invoice, k) == v

    @pytest.mark.parametrize("optional_field", ("description",))
    def test_required_fields(self, optional_field, creation_data):
        creation_data.pop(optional_field)
        test_obj = Invoice.objects.create(**creation_data)
        assert test_obj.id

    @pytest.mark.parametrize("required_field", ("amount", "currency", "payment_type"))
    def test_required_field_absence_raises_error(self, required_field, creation_data):
        creation_data.pop(required_field)
        with pytest.raises(IntegrityError):
            Invoice.objects.create(**creation_data)
