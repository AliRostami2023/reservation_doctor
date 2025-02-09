from rest_framework import serializers
from .models import CategoryMagazine, Magazine, Review


class CategoryMagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMagazine
        fields = '__all__'


class MagazineSerializer(serializers.ModelSerializer):
    category = CategoryMagazineSerializer()

    class Meta:
        model = Magazine
        fields = '__all__'
        read_only_fields = ['author', 'slug', 'create_at']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.get_full_name')
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author', 'magazine', 'create_at']

    def create(self, validated_data):
        magazine = Magazine.objects.get(slug=self.context['magazine_slug'])
        return Review.objects.create(magazine=magazine, **validated_data)


class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['body']
