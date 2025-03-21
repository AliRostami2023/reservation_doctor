import uuid
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from core.models import CreateMixin, UpdateMixin, InformationUser
from .managers import UserManager
from .validators import MobileValidator


class User(AbstractBaseUser, PermissionsMixin, CreateMixin):
    full_name = models.CharField(_('نام و نام خانوادگی'), max_length=100)
    phone_number = models.CharField(_('شماره همراه'), max_length=11, unique=True, validators=[MobileValidator()])
    email = models.EmailField(_('ایمیل'), unique=True)

    USER_TYPE = (
        ('patient', _('بیمار')),
        ('doctor', _('پزشک'))
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE, verbose_name=_('نوع کاربر'))
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name', 'email']

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')


    def __str__(self):
        return self.full_name
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

class Doctor(CreateMixin, UpdateMixin, InformationUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', verbose_name=_('کاربر'))
    Medical_system_code = models.CharField(max_length=12, verbose_name=_('کد نظام پزشکی'))
    specialty = models.CharField(max_length=100, verbose_name=_('تخصص'))
    experience_years = models.PositiveSmallIntegerField(default=0, verbose_name=_('سابقه کاری'))

    def __str__(self):
        return self.user.full_name
    

    class Meta:
        verbose_name = _('پزشک')
        verbose_name_plural = _('پزشکان')


class Patient(CreateMixin, UpdateMixin, InformationUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_user', verbose_name=_('کاربر'))
    
    def __str__(self):
        return self.user.full_name
    

    class Meta:
        verbose_name = _('بیمار')
        verbose_name_plural = _('بیماران')



class OtpCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_otp", verbose_name=_('کاربر'))
    code = models.CharField(max_length=4, verbose_name=_('کد'))
    expired_date = models.DateTimeField(_('تاریخ انقضا'))

    def __str__(self):
        return self.user.full_name
    

    class Meta:
        verbose_name = _('کد تایید')
        verbose_name_plural = _('کد های تایید')

    
    def expired_date_over(self):
        return datetime.now() > self.expired_date

    def delete_otp(self):
        if self.expired_date_over():
            self.delete()
            return True
        return False


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset')
    token = models.UUIDField(unique=True, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


    def is_valid(self):
        return datetime.now() > self.created + timedelta(days=1) and not self.is_used
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = _('توکن ریست کلمه عبور')
        verbose_name_plural = _('توکن های ریست کلمه عبور')