from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator, EmailValidator
from django.db import models

class Utilisateur(AbstractUser):
    DEMANDEUR = 'Demandeur'
    PERCEPTEUR = 'Percepteur'
    SECRETAIRE = 'Secrétaire'
    NOTAIRE = 'Notaire'

    ROLE_CHOICES = (
        (DEMANDEUR, 'Demandeur'),
        (PERCEPTEUR, 'Percepteur'),
        (SECRETAIRE, 'Secrétaire'),
        (NOTAIRE, 'Notaire'),
    )

    # Champs supplémentaires
    profile_photo = models.ImageField(verbose_name='Photo de profil', upload_to='profile_photos/', null=True, blank=True)
    genre = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    telephone = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Le numéro de téléphone doit être entré au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
        )
    ])
    email = models.EmailField(validators=[EmailValidator()], verbose_name="Email")
    adresse = models.TextField(verbose_name="Adresse", null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Gestion des groupes en fonction du rôle de l'utilisateur
        if self.role == self.DEMANDEUR:
            group, _ = Group.objects.get_or_create(name='Demandeur')
            group.user_set.add(self)
        elif self.role == self.PERCEPTEUR:
            group, _ = Group.objects.get_or_create(name='Percepteur')
            group.user_set.add(self)
        elif self.role == self.SECRETAIRE:
            group, _ = Group.objects.get_or_create(name='Secrétaire')
            group.user_set.add(self)
        elif self.role == self.NOTAIRE:
            group, _ = Group.objects.get_or_create(name='Notaire')
            group.user_set.add(self)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
