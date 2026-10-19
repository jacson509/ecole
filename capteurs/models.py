from django.db import models
from django.core.validators import MinLengthValidator


class TypeCapteur(models.Model):
    nom = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "type de capteur"
        verbose_name_plural = "types de capteurs"

    def __str__(self):
        return self.nom


class Capteur(models.Model):
    nom = models.CharField(max_length=40, unique=True, validators=[MinLengthValidator(3)])
    type_capteur = models.ForeignKey(TypeCapteur, on_delete=models.PROTECT, related_name="capteurs")
    emplacement = models.CharField(max_length=60)
    actif = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "capteur"
        verbose_name_plural = "capteurs"

    def __str__(self):
        return self.nom
