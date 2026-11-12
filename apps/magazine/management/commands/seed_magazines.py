
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.account.models import User
from apps.magazine.models import CategoryMagazine, Magazine


ARTICLES = [
    {
        "category": "ایمپلنت و جراحی",
        "title": "همه چیز درباره ایمپلنت دندان؛ از مراحل تا مراقبت‌ها",
        "slug": "dental-implant-guide",
        "image": "article_implant.jpg",
        "tags": ["ایمپلنت", "جراحی دندان", "سلامت دهان"],
        "content": """
ایمپلنت دندان یکی از روش‌های رایج برای جایگزینی دندان‌های از دست رفته است.
در این روش، پایه‌ای سازگار با بدن در استخوان فک قرار می‌گیرد تا نقش ریشه
دندان را ایفا کند.

مراحل درمان معمولاً شامل معاینه اولیه، بررسی وضعیت استخوان فک، کاشت پایه،
دوره ترمیم و در نهایت نصب روکش است. زمان مورد نیاز برای هر مرحله به شرایط
دهان و سلامت عمومی فرد بستگی دارد.

مراقبت از بهداشت دهان، مراجعه منظم به دندانپزشک و رعایت توصیه‌های درمانی
در حفظ نتیجه درمان اهمیت زیادی دارد.

برای انتخاب روش مناسب، حتماً با دندانپزشک متخصص مشورت کنید.
""",
    },
    {
        "category": "دندانپزشکی کودکان",
        "title": "چطور از دندان‌های کودکان مراقبت کنیم؟",
        "slug": "children-dental-care",
        "image": "article_pediatric.jpg",
        "tags": ["دندانپزشکی کودکان", "دندان شیری", "بهداشت دهان"],
        "content": """
مراقبت از دندان‌ها بهتر است از زمان رویش اولین دندان شیری آغاز شود.
عادت‌های درست بهداشتی در دوران کودکی می‌توانند در سلامت دهان و دندان
در سال‌های بعد نقش مهمی داشته باشند.

مسواک زدن متناسب با سن کودک، محدود کردن خوراکی‌های شیرین و مراجعه منظم
به دندانپزشک از نکات مهم مراقبت از دندان‌های کودکان هستند.

والدین می‌توانند با تبدیل مسواک زدن به یک فعالیت جذاب و روزانه، کودک را
به رعایت بهداشت دهان تشویق کنند.

در صورت مشاهده لکه، درد یا تغییر رنگ دندان، بهتر است کودک توسط دندانپزشک
معاینه شود.
""",
    },
    {
        "category": "دندانپزشکی زیبایی",
        "title": "روش‌های نوین زیبایی دندان و اصلاح طرح لبخند",
        "slug": "modern-smile-design",
        "image": "article_cosmetic.jpg",
        "tags": ["زیبایی دندان", "لمینت", "اصلاح طرح لبخند"],
        "content": """
زیبایی لبخند تنها به سفید بودن دندان‌ها محدود نمی‌شود. تناسب دندان‌ها،
سلامت لثه، وضعیت فک و هماهنگی اجزای لبخند هم اهمیت دارند.

روش‌هایی مانند بلیچینگ، ونیرهای دندانی و درمان‌های ترمیمی می‌توانند
با توجه به شرایط هر فرد برای بهبود ظاهر لبخند مورد استفاده قرار بگیرند.

انتخاب روش درمان باید بر اساس معاینه، سلامت دندان‌ها و نظر دندانپزشک
انجام شود. همه روش‌های زیبایی برای همه افراد مناسب نیستند.

پیش از شروع درمان، درباره مزایا، محدودیت‌ها و مراقبت‌های هر روش
با پزشک خود صحبت کنید.
""",
    },
    {
        "category": "سلامت لثه",
        "title": "چگونه از بیماری‌های لثه پیشگیری کنیم؟",
        "slug": "gum-disease-prevention",
        "image": "article_gum.jpg",
        "tags": ["سلامت لثه", "جرم‌گیری", "بهداشت دهان"],
        "content": """
سلامت لثه بخش مهمی از سلامت دهان و دندان است. التهاب، قرمزی، خونریزی
هنگام مسواک زدن و بوی نامطبوع دهان می‌توانند از نشانه‌هایی باشند که
نیاز به بررسی دارند.

مسواک زدن منظم، استفاده صحیح از نخ دندان و مراجعه دوره‌ای به دندانپزشک
در پیشگیری از مشکلات لثه اهمیت دارند.

در صورت مشاهده خونریزی مداوم یا تورم لثه، بهتر است معاینه را به تعویق
نیندازید. تشخیص زودهنگام می‌تواند روند درمان را ساده‌تر کند.

اطلاعات این مقاله عمومی است و جایگزین معاینه تخصصی نیست.
""",
    },
]


class Command(BaseCommand):
    help = "Create sample magazine categories and articles with images"

    @transaction.atomic
    def handle(self, *args, **options):
        image_dir = Path(settings.BASE_DIR) / "seed_data" / "images"

        for item in ARTICLES:
            image_path = image_dir / item["image"]
            if not image_path.is_file():
                raise CommandError(f"Image not found: {image_path}")

        doctor_users = list(
            User.objects.filter(
                phone_number__in=[
                    "09130000001",
                    "09130000002",
                    "09130000003",
                    "09130000004",
                ],
                user_type="doctor",
            ).order_by("phone_number")
        )

        if len(doctor_users) != 4:
            raise CommandError(
                "Please run 'python manage.py seed_doctors' first."
            )

        created_count = 0
        existing_count = 0

        for index, item in enumerate(ARTICLES):
            category, _ = CategoryMagazine.objects.get_or_create(
                name=item["category"],
                defaults={"publish": True},
            )

            magazine, created = Magazine.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "category": category,
                    "author": doctor_users[index % len(doctor_users)],
                    "title": item["title"],
                    "content": item["content"].strip(),
                    "status": "publish",
                },
            )

            if not magazine.image:
                image_path = image_dir / item["image"]
                with image_path.open("rb") as image_file:
                    magazine.image.save(
                        item["image"],
                        File(image_file),
                        save=True,
                    )

            magazine.tags.add(*item["tags"])

            if created:
                created_count += 1
            else:
                existing_count += 1

            self.stdout.write(
                f"{magazine.title}: "
                f"{'created' if created else 'exists'}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Articles created: {created_count} | Existing: {existing_count}"
            )
        )
