from django.urls import path
from . import views

app_name = "capteurs"

urlpatterns = [
    path("", views.capteur_liste, name="liste"),
    path("types/", views.type_liste, name="types"),
    path("types/ajouter/", views.type_ajouter, name="type_ajouter"),
    path("types/<int:pk>/modifier/", views.type_modifier, name="type_modifier"),
    path("types/<int:pk>/supprimer/", views.type_supprimer, name="type_supprimer"),
    path("ajouter/", views.capteur_ajouter, name="ajouter"),
    path("<int:pk>/", views.capteur_detail, name="detail"),
    path("<int:pk>/modifier/", views.capteur_modifier, name="modifier"),
    path("<int:pk>/supprimer/", views.capteur_supprimer, name="supprimer"),
    path("<path:chemin_inconnu>/", views.page_inconnue, name="page_inconnue"),
]
