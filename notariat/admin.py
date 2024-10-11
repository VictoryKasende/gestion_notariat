from django.contrib import admin

from notariat.models import Document, Recu


# Personnaliser l'affichage de la liste pour le modèle Document
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'statut', 'date', 'demandeur')  # Champs à afficher dans la liste
    search_fields = ('nom', 'numero_reference', 'demandeur__username')  # Champs sur lesquels vous pouvez rechercher
    list_filter = ('type', 'statut', 'date', 'demandeur')  # Filtres à utiliser dans l'interface


class RecuAdmin(admin.ModelAdmin):
    list_display = ('numero_recu', 'montant', 'motif', 'date_recu', 'document')  # Champs à afficher dans la liste
    search_fields = ('numero_recu', 'document__nom', 'utilisateur__username')  # Champs sur lesquels vous pouvez rechercher
    list_filter = ('mode_paiement', 'date_recu', 'document')  # Filtres à utiliser dans l'interface


# Enregistrement des modèles avec l'admin de Django
admin.site.register(Document, DocumentAdmin)
admin.site.register(Recu, RecuAdmin)