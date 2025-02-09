from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, full_name, email, phone_number, password=None, **extra_fields):
        if not full_name:
            raise ValueError(_('نام ونام خانوادگی خود را وارد کنید'))
        
        if not email:
            raise ValueError(_('ایمیل خود را وارد کنید'))
        
        if not phone_number:
            raise ValueError(_('شماره همراه خود را وارد کنید'))
        
        user = self.model(
            full_name=full_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, phone_number, full_name, email, password, **extra_fields):
        user = self.create_user(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user
    