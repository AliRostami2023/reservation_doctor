from django.urls import path, re_path
from . import views


app_name = 'magazine'

urlpatterns = [
    path('', views.ListBlogAPIView.as_view(), name='blog_list'),
    re_path(r'^detail/(?P<slug>[-\wآ-ی]+)/', views.RetriveBlogAPIView.as_view(), name='blog_detail'),
    path('create/', views.CreateBlogAPIView.as_view(), name='create_blog'),
    path('update/<int:pk>/', views.UpdateBlogAPIView.as_view(), name='update_blog'),
    path('category_list/', views.ListCategoryBlogAPIView.as_view(), name='list_category_blog'),
    path('category/detail/<int:pk>', views.RetriveCategoryBlogAPIView.as_view(), name='category_blog_detail'),
    path('create_category/', views.CreateCategoryBlogAPIView.as_view(), name='create_category_blog'),
    path('update_category/<int:pk>/', views.UpdateCategoryBlogAPIView.as_view(), name='update_category_blog'),
    re_path(r'^(?P<magazine_slug>[-\wآ-ی]+)/comments/', views.CommentBlogListAPIView.as_view(), name='comment-list'),
    re_path(r'^(?P<magazine_slug>[-\wآ-ی]+)/create_comment/', views.CommentBlogCreateAPIView.as_view(), name='comment-create'),
    re_path(r'^(?P<magazine_slug>[-\wآ-ی]+)/(?P<comment_id>\d+)/reply/', views.BlogReplyCreateAPIView.as_view(), name='comment-reply'),
    re_path(r'^(?P<magazine_slug>[-\wآ-ی]+)/(?P<pk>\d+)/edit/', views.CommentBlogUpdateDeleteAPIView.as_view(), name='comment-edit'),
    re_path(r'^(?P<magazine_slug>[-\wآ-ی]+)/replies/(?P<pk>\d+)/edit/', views.BlogReplyUpdateDeleteAPIView.as_view(), name='reply-edit'),
]
