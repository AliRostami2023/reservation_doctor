from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils.text import slugify
from core.models import CreateMixin, UpdateMixin


User = get_user_model()


class CategoryMagazine(CreateMixin, UpdateMixin):
    name = models.CharField(_('نام دسته بندی'), max_length=200)
    publish = models.BooleanField(default=True, verbose_name=_('منتشر شود'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('اضافه کردن یا ویرایش دسته بندی')
        verbose_name_plural = _('دسته بندی مجله ها')


class Magazine(CreateMixin, UpdateMixin):
    category = models.ForeignKey(CategoryMagazine, on_delete=models.CASCADE, related_name='categories', verbose_name=_('دسته بندی'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_blog", verbose_name=_('نویسنده'))
    title = models.CharField(max_length=500, verbose_name=_('عنوان مجله'))
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True, verbose_name=_('اسلاگ'))
    image = models.ImageField(upload_to="image_magazine", null=True, blank=True, verbose_name=_('تصویر مقاله'))
    content = models.TextField(_('متن مقاله'))

    STATUS = (
        ('draft', _('پیش نویس مقاله')),
        ('publish', _('انتشار مقاله'))
    )

    status = models.CharField(max_length=30, choices=STATUS, default='publish', verbose_name=_('وضعیت'))

    tags = TaggableManager()

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Magazine.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'مجله'
        verbose_name_plural = 'مجلات'



class Review(CreateMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_review", verbose_name=_('نویسنده'))
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, related_name="blog_review", verbose_name=_('مقاله'))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True, verbose_name=_('پاسخ دیدگاه'))
    body = models.TextField(_('متن دیدگاه'))
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                 null=True, blank=True, default=0, verbose_name=_('امتیاز'))
    
    def __str__(self):
        return f'{self.author} commented in {self.magazine}'

    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'
        ordering = ('-create_at',)
