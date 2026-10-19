from django.contrib import admin
from django.urls import include, path
from capteurs.views import page_inconnue

handler404 = "capteurs.views.page_inconnue"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("capteurs.urls")),
]
