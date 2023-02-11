from rest_framework import filters

from users.permissions import IsAdminOrReadOnly  # isort:skip


class CommonViewSetMixin:
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class NoAuthorUpdateMixin:

    def perform_update(self, serializer):
        """
        Для предотвращения подмены автора объекта при использовании
        метода PATCH удаляем из валидированных данных ключ 'автор'.
        """
        serializer.validated_data.pop("author", None)
        super().perform_update(serializer)  # type:ignore
