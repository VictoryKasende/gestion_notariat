from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def is_notaire(user):
    return user.role == 'Notaire'


@login_required
@user_passes_test(is_notaire)
def notariat(request):
    return render(request, 'notariat/notarier_document.html')

@login_required
@user_passes_test(is_notaire)
def save(request):
    return render(request, 'notariat/save_document.html')


@login_required
@user_passes_test(is_notaire)
def gerer(request):
    return render(request, 'notariat/gerer_document.html')


@login_required
@user_passes_test(is_notaire)
def paiement(request):
    return render(request, 'notariat/payement_document.html')

@login_required
@user_passes_test(is_notaire)
def rapport(request):
    return render(request, 'notariat/rapport_document.html')

@login_required
@user_passes_test(is_notaire)
def voir(request):
    return render(request, 'notariat/detail_document.html')

@login_required
@user_passes_test(is_notaire)
def add_demandeur(request):
    return render(request, 'notariat/add_demandeur.html')