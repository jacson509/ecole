from django import forms
from .models import Capteur, TypeCapteur


class RechercheCapteurForm(forms.Form):
    q = forms.CharField(required=False, max_length=40, label="Nom / modèle du capteur", widget=forms.TextInput(attrs={"placeholder": "Ex. DHT22, PIR, MQ-7"}))
    actifs_seulement = forms.BooleanField(required=False, label="Actifs seulement")


class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = ["nom", "type_capteur", "emplacement", "actif", "description"]
        labels = {"nom": "Nom / modèle du capteur", "type_capteur": "Catégorie fonctionnelle", "emplacement": "Emplacement", "actif": "Capteur actif", "description": "Description"}
        widgets = {"nom": forms.TextInput(attrs={"placeholder": "Ex. DHT22, PIR, MQ-7, LDR, HC-SR04"}), "description": forms.Textarea(attrs={"rows": 4})}
        help_texts = {"nom": "Indiquez le modèle du matériel, par exemple DHT22, PIR, MQ-7 ou LDR."}


class TypeCapteurForm(forms.ModelForm):
    class Meta:
        model = TypeCapteur
        fields = ["nom", "description"]
        labels = {"nom": "Catégorie (ex. Mouvement, Température, Gaz)", "description": "Description"}
        help_texts = {"nom": "Indiquez ce que le capteur mesure ou détecte, pas son modèle."}
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}
