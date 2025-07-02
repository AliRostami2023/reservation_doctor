from django.conf import settings
from kavenegar import *
from celery import shared_task


@shared_task()
def send_otp_register(phone_number, otp):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API)
        params = {
            'sender': '', #optional
            'receptor': phone_number,
            'message': f'کد تایید احراز هویت شما n\ {otp}',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)
    