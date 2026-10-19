from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


def creer_types_existants(apps, schema_editor):
    TypeCapteur = apps.get_model("capteurs", "TypeCapteur")
    Capteur = apps.get_model("capteurs", "Capteur")
    anciens_types = [
        ("DHT22", "DHT22 — température / humidité", "Capteur de température et d'humidité"),
        ("LDR", "LDR — luminosité", "Capteur de luminosité"),
        ("PIR", "PIR — mouvement", "Détecteur de mouvement"),
        ("HC-SR04", "HC-SR04 — distance", "Capteur de distance ultrasonique"),
        ("BME280", "BME280 — température / humidité / pression", "Température, humidité et pression"),
        ("SHT40", "SHT40 — température / humidité", "Capteur de température et d'humidité"),
    ]
    mapping = {}
    for code, nom, description in anciens_types:
        obj, _ = TypeCapteur.objects.get_or_create(code=code, defaults={"nom": nom, "description": description})
        mapping[code] = obj.pk
    for capteur in Capteur.objects.all():
        if capteur.type_capteur in mapping:
            capteur.type_capteur_nouveau_id = mapping[capteur.type_capteur]
            capteur.save(update_fields=["type_capteur_nouveau"])


class Migration(migrations.Migration):
    dependencies = [("capteurs", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="TypeCapteur",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ("code", models.SlugField(help_text="Code court, par exemple DHT22 ou PIR.", max_length=15, unique=True)),
                ("description", models.CharField(blank=True, max_length=160)),
            ],
            options={"verbose_name": "type de capteur", "verbose_name_plural": "types de capteurs", "ordering": ["nom"]},
        ),
        migrations.AddField(
            model_name="capteur", name="type_capteur_nouveau",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="capteurs_nouveaux", to="capteurs.typecapteur"),
        ),
        migrations.RunPython(creer_types_existants, migrations.RunPython.noop),
        migrations.RemoveField(model_name="capteur", name="type_capteur"),
        migrations.RenameField(model_name="capteur", old_name="type_capteur_nouveau", new_name="type_capteur"),
        migrations.AlterField(
            model_name="capteur", name="type_capteur",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="capteurs", to="capteurs.typecapteur"),
        ),
        migrations.AlterModelOptions(name="capteur", options={"ordering": ["nom"], "verbose_name": "capteur", "verbose_name_plural": "capteurs"}),
    ]
