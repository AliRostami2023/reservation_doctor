from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('category', views.CategoryMagazineViewSet, basename='category')
router.register('magazine', views.MagazineViewSet, basename='magazine')
router.register('review', views.ReviewViewSet, basename='review')

app_name = 'magazine'

urlpatterns = router.urls
