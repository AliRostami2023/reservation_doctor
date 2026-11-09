import json
from django.core.cache import cache
from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.account.models import User
from apps.account.random_code_otp import random_otp_code
from apps.utils.send_sms_otp import send_otp_register

OTP_TTL_SECONDS = 180


def start_patient_registration(*, validated_data):
    """Cache validated registration data and dispatch the verification OTP."""
    data = dict(validated_data)
    phone_number = data['phone_number']
    data.update(user_type='patient', otp=random_otp_code())
    cache.set(f'otp_registration:{phone_number}', json.dumps(data), timeout=OTP_TTL_SECONDS)
    send_otp_register.delay(phone_number, data['otp'])
    return data['otp']


@transaction.atomic
def complete_patient_registration(*, phone_number, code):
    key = f'otp_registration:{phone_number}'
    cached = cache.get(key)
    if not cached:
        raise serializers.ValidationError({'detail': _('اطلاعات منقضی شده است.')})
    data = json.loads(cached)
    if str(data.get('otp')) != str(code):
        raise serializers.ValidationError({'code': _('کد وارد شده صحیح نیست.')})
    if User.objects.filter(phone_number=phone_number).exists():
        raise serializers.ValidationError({'phone_number': _('این شماره قبلاً ثبت شده است.')})
    user = User.objects.create_user(
        phone_number=data['phone_number'], email=data['email'],
        full_name=data['full_name'], password=data['password'], user_type='patient', is_active=True,
    )
    cache.delete(key)
    return user
