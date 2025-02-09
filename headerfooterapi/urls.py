from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("social_media", views.SocialMediaViewSet, basename='social_media')
router.register("footer_link", views.FooterLinkViewSet, basename='footer_link')
router.register("about_us", views.AboutUSViewSet, basename='about_us')
router.register("licenses", views.LicenseViewSet, basename='licenses')

app_name = 'header_footer'

urlpatterns = router.urls
