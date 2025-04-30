from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from PIL import Image


class MobileValidator(RegexValidator):
    regex = r"^09[0-9]{9}$"
    message = _(
        'شماره موبایل باید شامل 11 رقم باشد و با 09 شروع شود'
        'برای مثال  09171234567'
    )


class NationalCodeValidator(RegexValidator):
    regex = r"^[0-9]{10}$"
    message = _(
        'کد ملی باید شامل 10 عدد باشد'
        'برای مثال  1234567890'
    )


def validate_avatar_size(image):
    max_size_mb = 2
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(_(f"The image size should not exceed {max_size_mb} MB."))
    

def validate_avatar_dimensions(image):
    max_width = 3840
    max_height = 2160

    with Image.open(image) as img:
        width, height = img.size
        if width > max_width or height > max_height:
            raise ValidationError(_(
                f'The image dimensions should not exceed {max_width}x{max_height} pixels.'))