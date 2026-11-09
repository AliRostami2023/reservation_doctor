from rest_framework import serializers
from .models import *


class SocialMediaSerializers(serializers.ModelSerializer):
    class Meta:
        model = socialMedia
        fields = '__all__'


class FooterLinkBoxSerializers(serializers.ModelSerializer):
    class Meta:
        model = FooterBoxLink
        fields = '__all__'


class FooterLinkSerializers(serializers.ModelSerializer):
    footer_box_link = FooterLinkBoxSerializers()

    class Meta:
        model = FooterLink
        fields = '__all__'


class AboutUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'


class LicenseSerializers(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'
