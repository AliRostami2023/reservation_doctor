from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
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


class DoctorSimpleSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['full_name', 'avatar']

    def get_avatar(self, obj):
        request = self.context.get('request')
        doctor = getattr(obj, 'doctor_profile', None)
        if doctor and doctor.avatar:
            return request.build_absolute_uri(doctor.avatar.url) if request else doctor.avatar.url
        return None
    

class ListRetriveBlogSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    author = DoctorSimpleSerializer(read_only=True)
    comment_blog = CommentListSerializer(many=True, read_only=True, source='comments')
    time_since_created = serializers.SerializerMethodField()

    class Meta:
        model = Magazine
        fields = ['title', 'slug', 'author', 'category', 'image',
                   'content', 'comment_blog', 'create_at', 'update_at', 'time_since_created']


    def get_time_since_created(self, obj):
        now = timezone.now() 
        if obj.create_at is None:
            return None

        if timezone.is_naive(obj.create_at):
            create_at = timezone.make_aware(obj.create_at, timezone.get_default_timezone())
        else:
            create_at = obj.create_at

        diff = now - create_at
        days = diff.days
        hours = diff.seconds // 3600

        if days >= 1:
            return f"{days} روز پیش"
        elif hours >= 1:
            return f"{hours} ساعت پیش"
        else:
            return "کمتر از یک ساعت پیش"


class UpdateBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Magazine
		fields = ['title', 'category', 'image', 'content']
            
    

class CreateBlogSerializer(serializers.ModelSerializer):
     author = serializers.CharField(source='author.full_name', read_only=True)

     class Meta:
          model = Magazine
          fields = ['title', 'category', 'image', 'author', 'content', 'create_at', 'update_at']
