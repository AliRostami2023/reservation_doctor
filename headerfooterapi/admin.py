from django.contrib import admin
from .models import *


class FooterLinkInline(admin.TabularInline):
    model = FooterLink


@admin.register(socialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['instagram', 'telegram', 'twitter', 'whatsapp', 'facebook']


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['about_us', 'contact_us', 'copyright', 'logo_site']


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'link']


@admin.register(FooterBoxLink)
class FooterBoxLinkAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [FooterLinkInline]
