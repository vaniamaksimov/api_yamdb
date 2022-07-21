from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Review, Title, User
from .mixins import ListCreateDestroyViewSet, RetriveUpdateViewSet
from .permissions import IsAdminOrReadOnly, OwherAdminModeratorOrReadOnly
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer, TitlesSerializer,
                          UserMeSerializer, UserSerializer)


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
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = ('category', 'genre', 'name', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (OwherAdminModeratorOrReadOnly, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return serializer.save(title=title, author=self.request.user)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (OwherAdminModeratorOrReadOnly, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        rewiew_id = self.kwargs.get('rewiew_id')
        rewiew = get_object_or_404(Review, id=rewiew_id)
        return serializer.save(title=title,
                               rewiew=rewiew,
                               author=self.request.user)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, )
    filter_backends = (SearchFilter, )


class UserMeViewSet(RetriveUpdateViewSet):
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        user = self.request.user
        queryset = get_object_or_404(User, id=user.id)
        return queryset
