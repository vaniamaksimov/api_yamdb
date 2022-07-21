from django.db.models import Avg
from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SerializerMethodField,
                                        SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator


from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser as User


class CategoriesSerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitlesSerializer(ModelSerializer):
    rating = SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategoriesSerializer()

    class Meta:
        fields = ('name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class ReviewsSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True,
                              slug_field='username',
                              default=CurrentUserDefault())

    class Meta:
        fields = ('text',
                  'author',
                  'score',
                  'pub_date')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class CommentsSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('text',
                  'author',
                  'pub_date')
        model = Comment


class UserSerializer(ModelSerializer):

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class UserMeSerializer(ModelSerializer):

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
