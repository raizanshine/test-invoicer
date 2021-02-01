from http import HTTPStatus

from class_registry import RegistryKeyError
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from invoicer.invoices.payment_types import payment_registry, BasePaymentController
from invoicer.invoices.serializers import PaymentTypeSerializer, InvoiceSerializer


class PaymentTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = PaymentTypeSerializer
    pagination_class = None
    permission_classes = ()
    lookup_field = "label"

    def get_queryset(self):
        return payment_registry.values()

    def _get_payment_type(self, label):
        try:
            return payment_registry.get(label)
        except RegistryKeyError:
            raise NotFound()

    def get_object(self) -> BasePaymentController:
        label = self.kwargs.get("label")
        return self._get_payment_type(label)

    @action(methods=["post"], detail=False)
    def pay(self, request):
        invoice_serializer = InvoiceSerializer(data=request.data)
        invoice_serializer.is_valid(raise_exception=True)
        invoice_obj = invoice_serializer.save()
        payment_type = self._get_payment_type(request.data.get('payment_type'))
        payment_url = payment_type.get_payment_url(invoice_obj)
        return Response(data={"redirect": payment_url}, status=HTTPStatus.CREATED)
