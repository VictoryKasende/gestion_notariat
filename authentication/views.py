from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, reverse, redirect

from authentication.forms import ProfilForm


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse('admin:index')

        # Redirection pour les Notaires vers une page spécifique
        if user.role == 'Notaire':
            return reverse('notariat:notarier')  # Modifiez cette URL pour la page appropriée

        # Redirection pour les Percepteurs vers une page spécifique
        elif user.role == 'Percepteur':
            return reverse('notariat:payer_document')  # Modifiez cette URL pour la page appropriée

        # Redirection pour les Secrétaires vers une page spécifique
        elif user.role == 'Secrétaire':
            return reverse('notariat:save_document')  # Modifiez cette URL pour la page appropriée

        # Redirection pour les Demandeurs vers une page spécifique
        elif user.role == 'Demandeur':
            return reverse('demandeur:dashboard')  # Modifiez cette URL pour la page appropriée

        # Redirection par défaut
        return super().get_success_url()


@login_required
def profil(request):
    user = request.user  # Récupérer l'utilisateur connecté
    context = {
        'user': user  # Passez l'utilisateur au contexte
    }
    return render(request, 'authentication/profil.html', context)


