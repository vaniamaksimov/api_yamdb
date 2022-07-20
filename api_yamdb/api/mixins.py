from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)


class ListCreateDestroyViewSet(GenericAPIView, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    """ViewSet для отображения списка, создания и удаления ресурса"""
    pass
