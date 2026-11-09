
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from account.models import User, Doctor, DentalSpecialty


DOCTORS = [
    {
        "full_name": "دکتر نگار احمدی",
        "phone": "09130000001",
        "email": "negar.doctor@example.com",
        "password": "Test@123456",
        "code": "100000000001",
        "specialty": DentalSpecialty.ORTHODONTICS,
        "experience": 12,
        "birthday": "1986-04-12",
        "about": "متخصص ارتودانتیکس با بیش از ۱۲ سال تجربه در درمان ناهنجاری‌های فک و دندان. ارائه‌دهنده درمان‌های ارتودنسی ثابت و متحرک.",
        "address": "تهران، سعادت‌آباد، خیابان سرو",
        "image": "doctor_1.jpg",
    },
    {
        "full_name": "دکتر آرمان رضایی",
        "phone": "09130000002",
        "email": "arman.doctor@example.com",
        "password": "Test@123456",
        "code": "100000000002",
        "specialty": DentalSpecialty.IMPLANTOLOGY,
        "experience": 15,
        "birthday": "1982-08-20",
        "about": "متخصص ایمپلنت و جراحی‌های پیشرفته دهان و دندان با تمرکز بر درمان‌های دقیق و حفظ سلامت دهان.",
        "address": "تهران، ونک، خیابان ملاصدرا",
        "image": "doctor_2.jpg",
    },
    {
        "full_name": "دکتر سارا محمدی",
        "phone": "09130000003",
        "email": "sara.doctor@example.com",
        "password": "Test@123456",
        "code": "100000000003",
        "specialty": DentalSpecialty.PEDIATRIC_DENTISTRY,
        "experience": 9,
        "birthday": "1990-02-15",
        "about": "متخصص دندانپزشکی کودکان، با تجربه در درمان پوسیدگی دندان‌های شیری و ایجاد تجربه‌ای آرام برای کودکان.",
        "address": "تهران، پاسداران، خیابان گلستان",
        "image": "doctor_3.jpg",
    },
    {
        "full_name": "دکتر محمد کریمی",
        "phone": "09130000004",
        "email": "mohammad.doctor@example.com",
        "password": "Test@123456",
        "code": "100000000004",
        "specialty": DentalSpecialty.RESTORATIVE_ESTHETIC,
        "experience": 11,
        "birthday": "1987-11-03",
        "about": "متخصص دندانپزشکی ترمیمی و زیبایی، فعال در زمینه اصلاح طرح لبخند، ترمیم دندان و درمان‌های زیبایی.",
        "address": "تهران، جردن، خیابان نلسون ماندلا",
        "image": "doctor_4.jpg",
    },
]


class Command(BaseCommand):
    help = "Create sample doctors with profile images"

    @transaction.atomic
    def handle(self, *args, **options):
        image_dir = Path(settings.BASE_DIR) / "seed_data" / "images"

        for item in DOCTORS:
            image_path = image_dir / item["image"]
            if not image_path.is_file():
                raise CommandError(f"Image not found: {image_path}")

        created_count = 0
        existing_count = 0

        for item in DOCTORS:
            user, user_created = User.objects.get_or_create(
                phone_number=item["phone"],
                defaults={
                    "full_name": item["full_name"],
                    "email": item["email"],
                    "user_type": "doctor",
                    "is_active": True,
                },
            )

            if user.user_type != "doctor":
                raise CommandError(
                    f"{user.phone_number} already belongs to a non-doctor user."
                )

            if user_created:
                user.set_password(item["password"])
                user.save(update_fields=["password"])

            doctor, doctor_created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    "Medical_system_code": item["code"],
                    "specialty": item["specialty"],
                    "experience_years": item["experience"],
                    "brithday": item["birthday"],
                    "about_me": item["about"],
                    "address": item["address"],
                },
            )

            if not doctor.avatar:
                image_path = image_dir / item["image"]
                with image_path.open("rb") as image_file:
                    doctor.avatar.save(
                        item["image"],
                        File(image_file),
                        save=True,
                    )

            if user_created or doctor_created:
                created_count += 1
            else:
                existing_count += 1

            self.stdout.write(
                f"{doctor.user.full_name}: "
                f"{'created' if doctor_created else 'exists'}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Doctors created: {created_count} | Existing: {existing_count}"
            )
        )
