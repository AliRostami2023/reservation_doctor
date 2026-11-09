from apps.magazine.models import CategoryMagazine, Magazine, Review


def published_categories():
    return CategoryMagazine.objects.filter(publish=True).order_by('name')


def published_articles():
    return Magazine.objects.filter(status='publish').select_related('category', 'author__doctor_profile')


def article_reviews(slug):
    return Review.objects.filter(magazine__slug=slug, reply__isnull=True).select_related('author', 'magazine').prefetch_related('replies__author')
