from http import HTTPStatus

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from invoicer.invoices.models import InvoiceCurrency, Invoice
from invoicer.invoices.payment_types import (
    PayPalPaymentController,
    MasterCardPaymentController,
)


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class TestPaymentTypeView:
    def test_payment_types_list(self, client):
        response = client.get(reverse("payment_types-list"))
        expected_result = [
            {
                "label": MasterCardPaymentController.label,
                "is_enabled": MasterCardPaymentController.is_enabled,
                "domestic_url": MasterCardPaymentController.domestic_url,
            },
            {
                "label": PayPalPaymentController.label,
                "is_enabled": PayPalPaymentController.is_enabled,
                "domestic_url": PayPalPaymentController.domestic_url,
            },
        ]
        assert sorted(response.json(), key=lambda x: x["label"]) == expected_result

    @pytest.mark.parametrize("method", ("put", "post", "delete"))
    def test_payment_unsafe_methods_prohibited(self, method, client):
        response = getattr(client, method)(reverse("payment_types-list"))
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, response.json()

    def test_payment_type_detail_page_returns_object(self, client):
        expected_result = {
            "label": MasterCardPaymentController.label,
            "is_enabled": MasterCardPaymentController.is_enabled,
            "domestic_url": MasterCardPaymentController.domestic_url,
        }
        response = client.get(
            reverse(
                "payment_types-detail",
                kwargs={"label": MasterCardPaymentController.label},
            )
        )
        assert response.status_code == HTTPStatus.OK, response.json()
        assert response.json() == expected_result

    def test_unknown_payment_type_detail_raises_error(self, client):
        response = client.get(reverse("payment_types-detail", kwargs={"label": "visa"}))
        assert response.status_code == HTTPStatus.NOT_FOUND, response.json()

    def test_successful_payment(self, client):
        data = {
            "payment_type": PayPalPaymentController.label,
            "amount": 14.50,
            "currency": InvoiceCurrency.EURO,
            "description": "Тестовый платеж",
        }
        assert Invoice.objects.count() == 0
        response = client.post(reverse("payment_types-pay"), data=data, format="json")

        invoice_obj = Invoice.objects.get()
        for k, v in data.items():
            assert getattr(invoice_obj, k) == v
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "redirect": f"https://paypal.com/pay/invoice{invoice_obj.id}"
        }

    @pytest.mark.parametrize(
        "corrupted_field,corrupted_value",
        (
            ("payment_type", "invalid"),
            ("payment_type", ""),
            ("payment_type", None),
            ("amount", -134.04),
            ("amount", 0),
            ("amount", None),
            ("currency", "INV"),
            ("currency", None),
        ),
    )
    def test_invalid_payment(self, client, corrupted_field, corrupted_value):
        data = {
            "payment_type": PayPalPaymentController.label,
            "amount": 14.50,
            "currency": InvoiceCurrency.EURO,
            "description": "Тестовый платеж",
            corrupted_field: corrupted_value,
        }
        response = client.post(reverse("payment_types-pay"), data=data, format="json")
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert corrupted_field in response.data
