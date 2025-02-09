from django.db import models
from django.utils.translation import gettext_lazy as _
from account.validators import NationalCodeValidator, validate_avatar_dimensions, validate_avatar_size



class CreateMixin(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))

    class Meta:
        abstract = True

class UpdateMixin(models.Model):
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('آخرین آپدیت'))

    class Meta:
        abstract = True


class InformationUser(models.Model):
    avatar = models.ImageField(upload_to="doctor_images/", null=True, blank=True,
                                validators=[validate_avatar_dimensions, validate_avatar_size],
                                  verbose_name=_('عکس پروفایل'))
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True, validators=[NationalCodeValidator()], verbose_name=_('کد ملی'))
    brithday = models.DateField(null=True, blank=True, verbose_name=_('تاریخ تولد'))
    about_me = models.TextField(_('درباره من'), null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('آدرس'))

    class Meta:
        abstract = True
