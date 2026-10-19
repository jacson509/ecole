from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CapteurForm, RechercheCapteurForm, TypeCapteurForm
from .models import Capteur, TypeCapteur


def capteur_liste(request):
    capteurs = Capteur.objects.select_related("type_capteur").all()
    form = RechercheCapteurForm(request.GET or None)
    if request.GET:
        if form.is_valid():
            if form.cleaned_data["q"]:
                capteurs = capteurs.filter(nom__icontains=form.cleaned_data["q"])
            if form.cleaned_data["actifs_seulement"]:
                capteurs = capteurs.filter(actif=True)
        else:
            capteurs = Capteur.objects.none()
    return render(request, "capteurs/capteur_liste.html", {"capteurs": capteurs, "form": form})


def capteur_detail(request, pk):
    capteur = get_object_or_404(Capteur.objects.select_related("type_capteur"), pk=pk)
    return render(request, "capteurs/capteur_detail.html", {"capteur": capteur})


def capteur_ajouter(request):
    form = CapteurForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        capteur = form.save()
        messages.success(request, "Le capteur a été ajouté.")
        return redirect("capteurs:detail", pk=capteur.pk)
    return render(request, "capteurs/capteur_form.html", {"form": form, "titre": "Ajouter un capteur"})


def capteur_modifier(request, pk):
    capteur = get_object_or_404(Capteur, pk=pk)
    form = CapteurForm(request.POST or None, instance=capteur)
    if request.method == "POST" and form.is_valid():
        capteur = form.save()
        messages.success(request, "Le capteur a été modifié.")
        return redirect("capteurs:detail", pk=capteur.pk)
    return render(request, "capteurs/capteur_form.html", {"form": form, "titre": f"Modifier {capteur.nom}"})


def capteur_supprimer(request, pk):
    capteur = get_object_or_404(Capteur, pk=pk)
    if request.method == "POST":
        nom = capteur.nom
        capteur.delete()
        messages.success(request, f"Le capteur « {nom} » a été supprimé.")
        return redirect("capteurs:liste")
    return render(request, "capteurs/capteur_confirm_delete.html", {"capteur": capteur})


def type_liste(request):
    types = TypeCapteur.objects.all()
    return render(request, "capteurs/type_liste.html", {"types": types})


def type_ajouter(request):
    form = TypeCapteurForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        type_capteur = form.save()
        messages.success(request, "Le type de capteur a été ajouté.")
        return redirect("capteurs:types")
    return render(request, "capteurs/type_form.html", {"form": form, "titre": "Ajouter un type de capteur"})


def type_modifier(request, pk):
    type_capteur = get_object_or_404(TypeCapteur, pk=pk)
    form = TypeCapteurForm(request.POST or None, instance=type_capteur)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Le type de capteur a été modifié.")
        return redirect("capteurs:types")
    return render(request, "capteurs/type_form.html", {"form": form, "titre": f"Modifier {type_capteur.nom}"})


def type_supprimer(request, pk):
    type_capteur = get_object_or_404(TypeCapteur, pk=pk)
    if request.method == "POST":
        try:
            nom = type_capteur.nom
            type_capteur.delete()
            messages.success(request, f"Le type « {nom} » a été supprimé.")
            return redirect("capteurs:types")
        except ProtectedError:
            messages.error(request, "Ce type est utilisé par au moins un capteur. Modifiez ou supprimez d'abord ces capteurs.")
            return redirect("capteurs:types")
    return render(request, "capteurs/type_confirm_delete.html", {"type_capteur": type_capteur})


def page_inconnue(request, exception=None, chemin_inconnu=""):
    return render(request, "capteurs/page_inconnue.html", {"chemin_inconnu": chemin_inconnu}, status=404)
