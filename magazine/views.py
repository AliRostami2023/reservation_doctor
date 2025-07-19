from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .serializers import *
from .models import *
from .paginations import MagazinePagination, ReviewPaginations
from account.permissions import IsDoctor


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
    


class ListBlogAPIView(generics.ListAPIView):
    queryset = Magazine.objects.select_related('category')
    serializer_class = ListRetriveBlogSerializer
    pagination_class = MagazinePagination


class RetriveBlogAPIView(generics.RetrieveAPIView):
    queryset = Magazine.objects.select_related('category')
    serializer_class = ListRetriveBlogSerializer
    lookup_field = 'slug'


class CreateBlogAPIView(generics.CreateAPIView):
    queryset = Magazine.objects.select_related('category')
    serializer_class = CreateBlogSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    


class UpdateBlogAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Magazine.objects.select_related('category')
    serializer_class = UpdateBlogSerializer
    permission_classes = [IsDoctor]

    def get_object(self):
        return Magazine.objects.filter(user=self.request.user)


class CommentBlogListAPIView(generics.ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = ReviewPaginations

    def get_queryset(self):
        return Review.objects.filter(
            magazine__slug=self.kwargs['magazine_slug'],
            reply=None
        ).select_related('author', 'magazine', 'reply')


class CommentBlogCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        blog = get_object_or_404(Magazine, slug=self.kwargs['magazine_slug'])
        serializer.save(author=self.request.user, magazine=blog)


class BlogReplyCreateAPIView(generics.CreateAPIView):
    serializer_class = ReplyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        blog = get_object_or_404(Magazine, slug=self.kwargs['magazine_slug'])
        parent_comment = get_object_or_404(Review, pk=self.kwargs['comment_id'])

        if parent_comment.reply is not None:
            raise serializers.ValidationError("ریپلای روی ریپلای مجاز نیست.")

        serializer.save(author=self.request.user, magazine=blog, reply=parent_comment)


class CommentBlogUpdateDeleteAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return Review.objects.filter(
            blog__slug=self.kwargs['magazine_slug'],
            reply=None
        )


class BlogReplyUpdateDeleteAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ReplyUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return Review.objects.filter(
            blog__slug=self.kwargs['magazine_slug']
        ).exclude(reply=None)
    