from django.db import migrations, models
import django.core.validators


def convertir_types_en_categories(apps, schema_editor):
    """Remplace les anciens types nommés par modèles par des catégories fonctionnelles."""
    db = schema_editor.connection.alias
    TypeCapteur = apps.get_model("capteurs", "TypeCapteur")
    Capteur = apps.get_model("capteurs", "Capteur")

    anciens_types = list(TypeCapteur.objects.using(db).values("id", "code", "nom", "description"))
    categories = [
        ("Température", "Mesure la température. Certains modèles mesurent aussi l'humidité ou la pression."),
        ("Humidité", "Mesure l'humidité de l'air ou d'un milieu."),
        ("Mouvement", "Détecte un mouvement dans une zone."),
        ("Gaz", "Détecte la présence de certains gaz ou de fumée selon le modèle."),
        ("Luminosité", "Mesure ou détecte le niveau de lumière."),
        ("Distance", "Mesure une distance ou une présence à une distance donnée."),
        ("Pression", "Mesure la pression atmosphérique ou une autre pression selon le modèle."),
        ("Autre", "Catégorie à préciser selon la fonction du capteur."),
    ]
    category_ids = {}
    for nom, description in categories:
        code_temporaire = {
            "Température": "temperature",
            "Humidité": "humidite",
            "Mouvement": "mouvement",
            "Gaz": "gaz",
            "Luminosité": "luminosite",
            "Distance": "distance",
            "Pression": "pression",
            "Autre": "autre",
        }[nom]
        obj, _ = TypeCapteur.objects.using(db).get_or_create(
            nom=nom,
            defaults={"code": code_temporaire, "description": description},
        )
        category_ids[nom] = obj.pk

    code_to_category = {
        "DHT22": "Température",
        "BME280": "Température",
        "SHT40": "Température",
        "PIR": "Mouvement",
        "HC-SR04": "Distance",
        "LDR": "Luminosité",
    }
    old_ids = {item["id"]: code_to_category.get(item["code"], "Autre") for item in anciens_types}
    for old_id, category_name in old_ids.items():
        Capteur.objects.using(db).filter(type_capteur_id=old_id).update(
            type_capteur_id=category_ids[category_name]
        )

    # Supprime uniquement les anciens enregistrements; les capteurs ont déjà été réassociés.
    TypeCapteur.objects.using(db).filter(pk__in=list(old_ids.keys())).delete()


def retour_arriere(apps, schema_editor):
    # La migration inverse le schéma, mais les anciens noms de modèle ne peuvent pas
    # être reconstruits automatiquement à partir de catégories fonctionnelles.
    pass


class Migration(migrations.Migration):
    dependencies = [("capteurs", "0002_types_capteurs")]
    operations = [
        migrations.RunPython(convertir_types_en_categories, retour_arriere),
        migrations.RemoveField(model_name="typecapteur", name="code"),
        migrations.AlterField(
            model_name="typecapteur",
            name="nom",
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]
