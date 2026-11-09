from rest_framework import generics, permissions
from ..models import CategoryMagazine
from ..serializers import (ListRetriveCategoryBlogSerializer, CreateCategoryBlogSerializer,
    UpdateCategoryBlogSerializer)


class ListCategoryBlogAPIView(generics.ListAPIView):
    queryset = CategoryMagazine.objects.all()
    serializer_class = ListRetriveCategoryBlogSerializer


class RetriveCategoryBlogAPIView(generics.RetrieveAPIView):
    queryset = CategoryMagazine.objects.all()
    serializer_class = ListRetriveCategoryBlogSerializer


class CreateCategoryBlogAPIView(generics.CreateAPIView):
    queryset = CategoryMagazine.objects.all()
    serializer_class = CreateCategoryBlogSerializer
    permission_classes = [permissions.IsAdminUser]


class UpdateCategoryBlogAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = CategoryMagazine.objects.all()
    serializer_class = UpdateCategoryBlogSerializer
    permission_classes = [permissions.IsAdminUser]
