from django import forms
from django.contrib.auth import get_user_model

from notariat.models import Document

User = get_user_model()


from django import forms


class DemandeurForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'telephone', 'email', 'genre', 'profile_photo', 'username', 'adresse']
        widgets = {
            'genre': forms.RadioSelect(attrs={'class': 'custom-radio'}),
            'profile_photo': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'adresse': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        # Enlever le help_text du champ username
        help_texts = {
            'username': None,
        }

    def save(self, commit=True):
        # On définit le rôle automatiquement comme 'Demandeur'
        utilisateur = super().save(commit=False)
        utilisateur.role = User.DEMANDEUR
        if commit:
            utilisateur.save()
        return utilisateur


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'demandeur', 'type', 'statut', 'description']