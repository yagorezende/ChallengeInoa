from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from .utils.paginators import DefaultNumberPagination
from .utils.utils import get_proper_serializer


class MultiSerializerListApiView(ListAPIView):
    """
    Use this class to create a view that can return different serializers based on the query parameter "serializer".
    Also, this class will handle the hide/show logic for archived objects.
    To return archived objects use the query parameter "archived_status".

    IN: Remember to mark the should_check_status=False, in the case that the model does not have status field
    """

    basic_serializer_class = None
    aggregated_serializer_class = None
    should_check_status = True  # field to ignore the archived status filter
    pagination_class = DefaultNumberPagination
    hidden_status = ["archived"]
    order_by = "-id"

    def get_serializer_class(self):
        return get_proper_serializer(self, self.request)

    def get_queryset(self, *args, **kwargs):
        # check if the return should have archived objects or not
        if not self.should_check_status or self.request.query_params.get("archived_status"):
            return self.queryset.order_by(self.order_by)
        return self.queryset.exclude(status__in=self.hidden_status).order_by(self.order_by)


class MultiSerializerDetailApiView(RetrieveUpdateDestroyAPIView):
    """
    Use this class for READ|UPDATE|DELETE views
    """

    basic_serializer_class = None
    aggregated_serializer_class = None

    def get_serializer_class(self):
        return get_proper_serializer(self, self.request)

    def perform_destroy(self, instance):
        if hasattr(instance, "status"):
            instance.status = "archived"
            instance.save()
        else:
            instance.delete()
