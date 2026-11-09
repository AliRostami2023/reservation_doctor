from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import Magazine
from ..serializers import ListRetriveBlogSerializer, CreateBlogSerializer, UpdateBlogSerializer
from ..paginations import MagazinePagination
from apps.account.permissions import IsDoctor
from ..selectors.articles import published_articles


class ListBlogAPIView(generics.ListAPIView):
    queryset = published_articles()
    serializer_class = ListRetriveBlogSerializer
    pagination_class = MagazinePagination


class RetriveBlogAPIView(generics.RetrieveAPIView):
    queryset = published_articles()
    serializer_class = ListRetriveBlogSerializer
    lookup_field = 'slug'


class CreateBlogAPIView(generics.CreateAPIView):
    queryset = Magazine.objects.all()
    serializer_class = CreateBlogSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UpdateBlogAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = published_articles()
    serializer_class = UpdateBlogSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return Magazine.objects.select_related('category', 'author').filter(author=self.request.user)
