from main.models import MyBlog, Contact, Comment, Category
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (ModelSerializer)


class CommentNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения комментариев."""

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_data')


class CategoryNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения категорий."""

    class Meta:
        model = Category
        fields = ('id', 'name')


class BlogListSerializer(ModelSerializer):
    """Сериализатор для отображения постов."""
    category = CategoryNestedSerializer()

    class Meta:
        model = MyBlog
        fields = ('id', 'title', 'photo', 'content', 'time_create',
                  'time_update', 'read_counter', 'category', 'author')


class CommentListSerializer(ModelSerializer):
    """Сериализатор для отображения комментариев."""
    post = BlogListSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_date',
                  'approved_comment')


class PopularPostsSerializer(ModelSerializer):
    """Сериализатор для отображения популярных постов."""
    popular_posts = SerializerMethodField()

    class Meta:
        model = MyBlog
        fields = ('id', 'title', 'subtitle', 'description', 'read_counter',
                  'subsection_exist', 'subsections_count', 'articles_count',
                  'popular_posts')

    def get_popular_posts(self, obj):
        return BlogListSerializer(
            MyBlog.objects.order_by('-read_counter')[:3],
            many=True
        ).data


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('email', 'name', 'message')
