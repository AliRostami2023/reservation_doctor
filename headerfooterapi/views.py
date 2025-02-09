from rest_framework import permissions, viewsets
from .models import *
from .serializers import *


class SocialMediaViewSet(viewsets.ModelViewSet):
    queryset = socialMedia.objects.all()
    serializer_class = SocialMediaSerializers
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return super().get_permissions()
    

class FooterLinkViewSet(viewsets.ModelViewSet):
    queryset = FooterLink.objects.select_related('footer_box_link')
    serializer_class = FooterLinkSerializers
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return super().get_permissions()
    

class AboutUSViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializers
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return super().get_permissions()
    

class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializers
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return super().get_permissions()

    
