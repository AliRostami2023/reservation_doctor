import account.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_alter_passwordresettoken_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passwordresettoken",
            name="token",
            field=models.CharField(
                default=account.models.generate_password_reset_token,
                max_length=300,
                unique=True,
            ),
        ),
    ]
