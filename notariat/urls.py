from django.contrib.auth.views import LogoutView
from django.urls import path

from notariat import views

app_name = 'notariat'

urlpatterns = [
    path('noatarier/', views.notariat, name='notarier'),
    path('save/document/', views.save, name='save_document'),
    path('gerer/document/', views.gerer, name='gerer_document'),
    path('payer/document/', views.paiement, name='payer_document'),
    path('rapport/document/', views.rapport, name='rapport_document'),
    path('voir/document/', views.voir),
    path('add/demandeur/', views.add_demandeur),
]