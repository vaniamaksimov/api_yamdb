from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.db.models import Avg


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
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(many=True, read_only=True)

    class Meta:
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
        model = Titles

    def get_rating(self, obj):
        return obj.rewiews.aggregate(Avg('score'))


class ReviewsSerializer(ModelSerializer):

    class Meta:
        fields = ('text', 'author', 'score', 'pub_date')
        model = Reviews


class CommentsSerializer(ModelSerializer):

    class Meta:
        fields = ('text', 'author', 'pub_date')
        model = Comments


class UserSerializer(ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
