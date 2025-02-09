from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from .paginations import MagazinePagination, ReviewPaginations
from .permissions import IsAuthenticatedOrAdmin


class CategoryMagazineViewSet(viewsets.ModelViewSet):
    queryset = CategoryMagazine.objects.all()
    serializer_class = CategoryMagazineSerializer
    permission_classes = [permissions.IsAdminUser]


    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return super().get_permissions()


class MagazineViewSet(viewsets.ModelViewSet):
    queryset = Magazine.objects.select_related('author', 'category')
    serializer_class = MagazineSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MagazinePagination

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return super().get_permissions()
    

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrAdmin]
    pagination_class = ReviewPaginations

    def perform_create(self, serializer):
        serializer.save(self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return UpdateReviewSerializer
        return super().get_serializer_class()
    
    def get_serializer_context(self):
        return {'request': self.request, 'magazine_slug': self.kwargs['magazine_slug']}
    
    def get_queryset(self):
        return Review.objects.filter(magazine__slug=self.kwargs['magazine_slug']) \
                    .select_related('authoe', 'magazine', 'reply')
    
    
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    