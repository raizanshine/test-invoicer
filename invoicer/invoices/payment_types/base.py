import abc

from class_registry import ClassRegistry

from invoicer.invoices.models import Invoice


payment_registry = ClassRegistry(attr_name="label", unique=True)


class BasePaymentController(abc.ABC):
    # идентификатор платежной системы в реестре
    label = ""
    # определяет, доступна ли платежная система для использования
    is_enabled = True
    # ссылка на домашнюю страницу
    domestic_url = ""

    def get_payment_url(self, invoice: Invoice):
        """
        Возвращает ссылку для оплаты для счета invoice
        """
        raise NotImplementedError
