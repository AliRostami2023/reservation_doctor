from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta
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
    is_active = models.BooleanField(default=False)

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
    



class DentalSpecialty(models.TextChoices):
    """
    Choices for dental specialties, available in both English and Persian.
    """
    ORTHODONTICS = 'ORTHO', _('ارتودانتیکس')
    PERIODONTICS = 'PERIO', _('پریودانتیکس')
    ENDODONTICS = 'ENDO', _('اندودانتیکس')
    PROSTHODONTICS = 'PROS', _('پروتزهای دندانی')
    ORAL_MAXILLOFACIAL_SURGERY = 'OMFS', _('جراحی فک و صورت')
    PEDIATRIC_DENTISTRY = 'PED', _('دندانپزشکی کودکان')
    RESTORATIVE_ESTHETIC = 'REST', _('دندانپزشکی ترمیمی و زیبایی')
    ORAL_MAXILLOFACIAL_RADIOLOGY = 'OMFR', _('رادیولوژی فک و صورت')
    ORAL_MAXILLOFACIAL_PATHOLOGY = 'OMFP', _('آسیب‌شناسی فک و صورت')
    DENTAL_PUBLIC_HEALTH = 'DPH', _('بهداشت عمومی دندان')
    IMPLANTOLOGY = 'IMPL', _('ایمپلنتولوژی')



class Doctor(CreateMixin, UpdateMixin, InformationUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', verbose_name=_('کاربر'))
    Medical_system_code = models.CharField(max_length=12, verbose_name=_('کد نظام پزشکی'))
    specialty = models.CharField(
        max_length=30, 
        choices=DentalSpecialty.choices,
        verbose_name=_('تخصص')
    )
    experience_years = models.PositiveSmallIntegerField(default=0, verbose_name=_('سابقه کاری'))

    def __str__(self):
        return self.user.full_name
    

    class Meta:
        verbose_name = _('پزشک')
        verbose_name_plural = _('پزشکان')


class Patient(CreateMixin, UpdateMixin, InformationUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_user', verbose_name=_('کاربر'))
    GENDER = (
        ('male', 'مرد'),
        ('female', 'زن')
    )

    gender = models.CharField(max_length=6, choices=GENDER, null=True, blank=True, verbose_name=_('جنسیت'))
    
    def __str__(self):
        return self.user.full_name
    

    class Meta:
        verbose_name = _('بیمار')
        verbose_name_plural = _('بیماران')


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset')
    token = models.CharField(max_length=300, unique=True, default=get_random_string(250))
    created = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


    def is_valid(self):
        return timezone.now() > self.created + timedelta(days=1) and not self.is_used
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = _('توکن ریست کلمه عبور')
        verbose_name_plural = _('توکن های ریست کلمه عبور')
        