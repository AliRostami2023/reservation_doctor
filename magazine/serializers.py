from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CategoryMagazine, Magazine, Review


User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['full_name', 'avatar']

    def get_avatar(self, obj):
        request = self.context.get('request')
        profile = getattr(obj, 'profile', None)
        if profile and profile.avatar:
            return request.build_absolute_uri(profile.avatar.url) if request else profile.avatar.url
        return None


class ReplyListSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer()

    class Meta:
        model = Review
        fields = ['id', 'body', 'create_at', 'author']


class CommentListSerializer(serializers.ModelSerializer):
    magazine = serializers.CharField(source='magazine.title')
    author = UserSimpleSerializer()
    reply = serializers.SerializerMethodField(method_name='get_reply')

    class Meta:
        model = Review
        fields = ['id', 'body', 'create_at', 'author', 'magazine', 'reply']

    def get_reply(self, obj):
        replies = obj.replies.all()
        return ReplyListSerializer(replies, many=True, context=self.context).data
	

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['body']


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['body']


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['body']


class ReplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['body']


class ListRetriveCategoryBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = CategoryMagazine
		fields = '__all__'
            

class CreateCategoryBlogSerializer(serializers.ModelSerializer):
      class Meta:
        model = CategoryMagazine
        fields = '__all__'


class UpdateCategoryBlogSerializer(serializers.ModelSerializer):
      class Meta:
        model = CategoryMagazine
        fields = '__all__'


class ListRetriveBlogSerializer(serializers.ModelSerializer):
    category = ListRetriveCategoryBlogSerializer()
    author = serializers.CharField(source='author.full_name')
    comment_blog = CommentListSerializer(many=True, read_only=True, source='comments')

    class Meta:
        model = Magazine
        fields = ['title', 'slug', 'author', 'category', 'content', 'comment_blog', 'create_at', 'update_at']


	# def get_image(self, obj):
	# 	if isinstance(obj.image, Image):
	# 		return obj.image.image.url if obj.image.image else None
	# 	return None


class UpdateBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Magazine
		fields = ['title', 'category', 'content']
            

class CreateBlogSerializer(serializers.ModelSerializer):
     author = serializers.CharField(source='author.full_name', read_only=True)

     class Meta:
          model = Magazine
          fields = ['title', 'category', 'author', 'content', 'create_at', 'update_at']
