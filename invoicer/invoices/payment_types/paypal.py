from .base import BasePaymentController, payment_registry


@payment_registry.register("paypal")
class PayPalPaymentController(BasePaymentController):
    label = "paypal"
    domestic_url = "https://paypal.ru/"

    def get_payment_url(self, invoice: "Invoice"):
        return f"https://paypal.com/pay/invoice{invoice.id}"
