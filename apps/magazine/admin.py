from django.contrib import admin
from .models import CategoryMagazine, Magazine, Review



class ReviewInline(admin.TabularInline):
    model = Review


@admin.register(CategoryMagazine)
class CategoryMagazineAdmin(admin.ModelAdmin):
    list_display = ["name", "publish"]


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author']
    list_filter = ['category']
    search_fields = ['title', 'author']
    inlines = [ReviewInline]
