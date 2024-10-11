from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Document(models.Model):
    # Définition des choix pour le type de document
    TYPE_ACTE = 'Acte'
    TYPE_CONTRAT = 'Contrat'
    TYPE_FACTURE = 'Facture'
    TYPE_RAPPORT = 'Rapport'

    # Liste des choix possibles pour le champ 'type'
    TYPE_CHOICES = [
        (TYPE_ACTE, 'Acte'),
        (TYPE_CONTRAT, 'Contrat'),
        (TYPE_FACTURE, 'Facture'),
        (TYPE_RAPPORT, 'Rapport'),
    ]

    # Définition des choix pour le statut du document
    STATUT_ATTENTE = 'En attente'
    STATUT_PAYE = 'Payé'
    STATUT_NOTARIE = 'Notarié'
    STATUT_ARCHIVE = 'Archivé'

    # Liste des choix possibles pour le champ 'statut'
    STATUT_CHOICES = [
        (STATUT_ATTENTE, 'En attente'),
        (STATUT_PAYE, 'Payé'),
        (STATUT_NOTARIE, 'Notarié'),
        (STATUT_ARCHIVE, 'Archivé'),
    ]

    # Définition des champs du modèle
    demandeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents_demandeur",
                                  verbose_name="Demandeur")  # Utilisateur associé en tant que demandeur
    secretaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents_secretaire",
                                   verbose_name="Secrétaire", blank=True,
                                   null=True)  # Utilisateur associé en tant que secrétaire
    nom = models.CharField(max_length=255, verbose_name="Nom du document")
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, verbose_name="Type de document")
    date = models.DateField(verbose_name="Date d'enregistrement", auto_now_add=True)
    statut = models.CharField(max_length=100, choices=STATUT_CHOICES, verbose_name="Statut du document")
    commentaire = models.TextField(verbose_name="Commentaire", null=True, blank=True)

    # Champs supplémentaires
    numero_reference = models.CharField(max_length=50, verbose_name="Numéro de référence", unique=True)
    description = models.TextField(verbose_name="Description détaillée", null=True, blank=True)
    fichier = models.FileField(upload_to='documents/', verbose_name="Fichier associé", null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()}) - {self.get_statut_display()}"


class Recu(models.Model):
    # Champs spécifiques pour les informations de paiement
    numero_recu = models.CharField(max_length=100, verbose_name="Numéro du reçu",
                                   unique=True)  # Numéro unique pour chaque reçu
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")  # Montant payé
    motif = models.CharField(max_length=255, verbose_name="Motif du paiement")  # Motif ou raison du paiement
    date_recu = models.DateField(verbose_name="Date de réception", auto_now_add=True)  # Date à laquelle le paiement a été effectué

    # Relation avec le modèle Document (un reçu est lié à un seul document)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="recus", verbose_name="Document")

    # Champs supplémentaires pour plus d'informations
    mode_paiement = models.CharField(
        max_length=50,
        choices=[
            ('Espèces', 'Espèces'),
            ('Carte bancaire', 'Carte bancaire'),
            ('Virement', 'Virement'),
            ('Chèque', 'Chèque'),
        ],
        verbose_name="Mode de paiement"
    )
    description = models.TextField(verbose_name="Description supplémentaire", null=True, blank=True)

    # Ajout d'une référence pour l'utilisateur ayant émis le reçu
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Émis par",
                                    related_name="recus")

    def __str__(self):
        return f"Reçu {self.numero_recu} pour {self.document.nom} - {self.montant} €"
