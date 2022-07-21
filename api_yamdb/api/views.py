from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly, OwherAdminOrReadOnly
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer, TitlesSerializer)


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class TitlesViewSet(ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = ('category', 'genre', 'name', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (OwherAdminOrReadOnly, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        queryset = title.reviews.all()
        return queryset


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserMeViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = get_object_or_404(User, id=user.id)
        return queryset
