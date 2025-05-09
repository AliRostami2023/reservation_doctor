from rest_framework.throttling import SimpleRateThrottle



class PhoneNumberRateThrottle(SimpleRateThrottle):
    scope = 'sms_code'

    def get_cache_key(self, request, view):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': phone_number
        }



class EmailResetThrottle(SimpleRateThrottle):
    scope = 'reset_email'

    def get_cache_key(self, request, view):
        email = request.data.get('email')
        if not email:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': email
        }
    
    