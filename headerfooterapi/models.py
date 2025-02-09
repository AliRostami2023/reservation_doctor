from django.db import models
from django.utils.translation import gettext_lazy as _


class socialMedia(models.Model):
    facebook = models.URLField(_("فیسبوک"), null=True, blank=True)
    telegram = models.URLField(_("تلگرام"), null=True, blank=True)
    twitter = models.URLField(_("توییتر"), null=True, blank=True)
    whatsapp = models.URLField(_("واتس اپ"), null=True, blank=True)
    instagram = models.URLField(_("اینستاگرام"), null=True, blank=True)

    def __str__(self):
        return self.instagram
    
    class Meta:
        verbose_name = 'اضافه کردن لینک فضای مجازی'
        verbose_name_plural = 'سوشال مدیا'
    

class FooterBoxLink(models.Model):
    name = models.CharField(max_length=300, verbose_name=_('نام لینک'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'نام لینک فوتر'
        verbose_name_plural = 'نام های لینکهای فوتر'

    
class FooterLink(models.Model):
    footer_box_link = models.ForeignKey(FooterBoxLink, on_delete=models.CASCADE, related_name='footer', verbose_name=_('نام لینک فوتر'))
    link = models.URLField(_('لینک'))

    def __str__(self):
        return self.footer_box_link.name
    
    class Meta:
        verbose_name = 'لینک'
        verbose_name_plural = 'لینک ها'

    
class AboutUs(models.Model):
    about_us = models.TextField(_('درباره ما'))
    contact_us = models.TextField(_('ارتباط با ما'))
    copyright = models.TextField(_('متن کپی رایت'))
    logo_site = models.ImageField(upload_to='images/logo_site', verbose_name=_('لوگو سایت'))

    def __str__(self):
        return self.about_us[:20]
    
    class Meta:
        verbose_name = 'اضافه کردن درباره ما'
        verbose_name_plural = 'درباره ما'

    
class License(models.Model):
    name = models.CharField(max_length=300, verbose_name=_('نام مجوز'))
    icon = models.ImageField(upload_to='images/icon_license', verbose_name=_('عکس مجوز'))
    link = models.URLField(_('لینک مجوز'), null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'مجوز'
        verbose_name_plural = 'مجوزها'
