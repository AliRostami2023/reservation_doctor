
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.account.models import User, Patient


class Command(BaseCommand):
    help = "Create sample patients and users"

    USERS = [
        {
            "full_name": "علی رضایی",
            "phone_number": "09120000001",
            "email": "ali.patient@example.com",
            "user_type": "patient",
            "password": "Test@123456",
            "gender": "male",
        },
        {
            "full_name": "سارا محمدی",
            "phone_number": "09120000002",
            "email": "sara.patient@example.com",
            "user_type": "patient",
            "password": "Test@123456",
            "gender": "female",
        },
        {
            "full_name": "محمد کریمی",
            "phone_number": "09120000003",
            "email": "mohammad.patient@example.com",
            "user_type": "patient",
            "password": "Test@123456",
            "gender": "male",
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for item in self.USERS:
            user, created = User.objects.get_or_create(
                phone_number=item["phone_number"],
                defaults={
                    "full_name": item["full_name"],
                    "email": item["email"],
                    "user_type": item["user_type"],
                    "is_active": True,
                },
            )

            if created:
                user.set_password(item["password"])
                user.save()
                created_count += 1
            else:
                updated_count += 1

            if item["user_type"] == "patient":
                Patient.objects.get_or_create(
                    user=user,
                    defaults={"gender": item["gender"]},
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Users created: {created_count} | Existing users: {updated_count}"
            )
        )
