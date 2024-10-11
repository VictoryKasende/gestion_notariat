from django.contrib.auth.views import LogoutView
from django.urls import path

from notariat import views

app_name = 'notariat'

urlpatterns = [
    path('notarier/', views.notariat, name='notarier'),
    path('document/<int:document_id>/', views.voir, name='detail_document'),
    path('notarier_document/<int:id>/', views.notarier_document, name='notarier_document'),  # Ajoutez cette ligne
    path('save/document/', views.save_document, name='save_document'),
    path('gerer/document/', views.gerer_document, name='gerer_document'),
    path('modifier/<int:document_id>/', views.modifier_document, name='modifier_document'),
    path('supprimer/<int:document_id>/', views.supprimer_document, name='supprimer_document'),
    path('archiver/<int:document_id>/', views.archiver_document, name='archiver_document'),
    path('payer/document/', views.paiement, name='payer_document'),
    path('rapport-paiement/pdf/', views.rapport_paiement_pdf, name='rapport_paiement_pdf'),
    path('rapport/document/', views.rapport_paiement, name='rapport_document'),
    path('voir/document/', views.voir),
    path('add/demandeur/', views.add_demandeur, name='add_demandeur'),
]
