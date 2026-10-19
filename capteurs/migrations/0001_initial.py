from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Capteur",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nom",
                    models.CharField(
                        max_length=40,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(3)],
                    ),
                ),
                (
                    "type_capteur",
                    models.CharField(
                        choices=[
                            ("DHT22", "DHT22 — température / humidité"),
                            ("LDR", "LDR — luminosité"),
                            ("PIR", "PIR — mouvement"),
                            ("HC-SR04", "HC-SR04 — distance"),
                            ("BME280", "BME280 — température / humidité / pression"),
                            ("SHT40", "SHT40 — température / humidité"),
                        ],
                        max_length=10,
                    ),
                ),
                ("emplacement", models.CharField(max_length=60)),
                ("actif", models.BooleanField(default=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
    ]
