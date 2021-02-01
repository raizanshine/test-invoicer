from invoicer.invoices.models import Invoice
from invoicer.invoices.payment_types.base import BasePaymentController, payment_registry


@payment_registry.register
class MasterCardPaymentController(BasePaymentController):
    label = "master_card"
    domestic_url = "https://mastercard.ru/"

    def get_payment_url(self, invoice: Invoice):
        return f"https://master-card.ru/pay/invoice{invoice.id}&sum={invoice.amount}"
