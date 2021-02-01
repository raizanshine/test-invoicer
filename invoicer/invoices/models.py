from django.db import models


class InvoiceCurrency(models.TextChoices):
    EURO = "EUR", "Евро"
    DOLLARS = "USD", "Доллары"
    ROUBLES = "RUB", "Рубли"


class Invoice(models.Model):
    amount = models.DecimalField(
        verbose_name="Сумма",
        null=False,
        blank=False,
        help_text="Сумма к оплате",
        decimal_places=2,
        max_digits=18,
    )
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    currency = models.CharField(
        verbose_name="Валюта",
        default=None,
        null=False,
        blank=False,
        max_length=9,
        choices=InvoiceCurrency.choices,
    )
    payment_type = models.CharField(
        verbose_name="Платежная система",
        default=None,
        null=False,
        blank=False,
        max_length=128,
    )

    def __str__(self):
        return f"Invoice #{self.id} in {self.amount} {self.currency}"
