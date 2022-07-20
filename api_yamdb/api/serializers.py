from rest_framework.serializers import ModelSerializer


class CategoriesSerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitlesSerializer(ModelSerializer):
    rating = None # среднее всех ревью
    description = None # Откуда брать информацию. Из стороннего АПИ?
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(many=True, read_only=True)

    class Meta:
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
        model = Titles


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
