from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import Utilisateur


class UtilisateurAdmin(UserAdmin):
    # Colonnes affichées dans la liste d'utilisateurs dans l'interface admin
    list_display = ('username', 'first_name', 'last_name', 'email', 'telephone', 'role', 'is_active', 'is_staff')

    # Champs par lesquels l'admin peut rechercher un utilisateur
    search_fields = ('username', 'first_name', 'last_name', 'email', 'role')

    # Filtres disponibles dans la barre latérale de l'interface admin
    list_filter = ('role', 'is_active', 'is_staff')

    # Champs affichés dans le formulaire d'édition d'un utilisateur
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Section authentification de base
        ('Informations personnelles',
         {'fields': ('first_name', 'last_name', 'email', 'telephone', 'genre', 'profile_photo')}),
        # Section des infos personnelles
        ('Rôle et statut', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        # Section pour gérer les rôles et le statut de l'utilisateur
        ('Permissions', {'fields': ('groups', 'user_permissions')}),  # Permissions spécifiques de l'utilisateur
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),  # Informations de suivi
    )

    # Champs affichés lors de l'ajout d'un nouvel utilisateur via l'interface admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # Classes CSS pour un affichage plus large
            'fields': (
                'username', 'first_name', 'last_name', 'email', 'telephone', 'genre', 'role', 'password1', 'password2',
                'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Ordre des utilisateurs dans la liste de l'interface admin
    ordering = ('username',)


# Enregistrement du modèle Utilisateur avec la configuration personnalisée
admin.site.register(Utilisateur, UtilisateurAdmin)
