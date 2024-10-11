from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

from notariat.forms import DemandeurForm, DocumentForm
from notariat.models import Document, Recu
from datetime import datetime
import io

User = get_user_model()

DEMANDEUR = 'Demandeur'
PERCEPTEUR = 'Percepteur'
SECRETAIRE = 'Secrétaire'
NOTAIRE = 'Notaire'


def is_notaire(user):
    return user.role == NOTAIRE

def is_demandeur(user):
    return user.role == DEMANDEUR

def is_percepteur(user):
    return user.role == PERCEPTEUR

def is_secretaire(user):
    return user.role == SECRETAIRE


@login_required
@user_passes_test(is_notaire)
def notariat(request):
    # Récupération des documents à notarier avec le statut "Payé"
    documents_a_notarier = Document.objects.filter(statut=Document.STATUT_PAYE)

    context = {
        'documents': documents_a_notarier,
        'total_documents': Document.objects.count(),
        'total_en_attente': documents_a_notarier.count(),
        'total_notaries_mois': Document.objects.filter(statut=Document.STATUT_NOTARIE).count(),
        # À ajuster pour le mois en cours
    }

    return render(request, 'notariat/notarier_document.html', context)


@login_required
@user_passes_test(is_notaire)
def notarier_document(request, id):
    # Récupérer le document
    document = get_object_or_404(Document, id=id)

    # Changer le statut du document en "Notarier"
    document.statut = Document.STATUT_NOTARIE  # Assurez-vous que le statut existe dans votre modèle
    document.save()
    current_year = timezone.now().year
    # Créer le contexte pour le PDF
    context = {
        'document': document,
        'current_year': current_year,
    }

    # Charger le template PDF
    template = get_template('notariat/rapport_pdf.html')
    html = template.render(context)

    # Générer le fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="document_{document.nom}.pdf"'

    # Générer le PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)

    return response


@login_required
@user_passes_test(is_secretaire)
def save_document(request):
    if request.method == "POST":
        # Récupération des données du formulaire
        demandeur_id = request.POST.get('demandeur')
        nom_document = request.POST.get('document_name')
        numero_document = request.POST.get('document_number')
        type_document = request.POST.get('document_type')
        description = request.POST.get('description')
        fichier = request.FILES.get('fichier')

        # Récupération de l'objet demandeur (Utilisateur)
        demandeur = User.objects.get(id=demandeur_id)

        # Création d'un nouveau document
        document = Document(
            demandeur=demandeur,
            nom=nom_document,
            numero_reference=numero_document,
            type=type_document,
            statut=Document.STATUT_ATTENTE,  # Initialiser le statut à 'En attente'
            description=description,
            fichier=fichier  # Enregistrement du fichier
        )
        document.save()

        # Message de succès
        messages.success(request, "Le document a été enregistré avec succès.")
        return redirect('notariat:save_document')

    # Récupération des demandeurs
    demandeurs = User.objects.filter(role='Demandeur')

    return render(request, 'notariat/save_document.html', {
        'demandeurs': demandeurs,
        'TYPE_CHOICES': Document.TYPE_CHOICES  # Ajout des choix de type de document au contexte
    })


@login_required
@user_passes_test(is_secretaire)
def gerer_document(request):
    # Récupérer tous les documents à afficher dans la gestion
    documents = Document.objects.all()

    # Compter les documents archivés
    total_archived = Document.objects.filter(statut=Document.STATUT_ARCHIVE).count()

    context = {
        'documents': documents,
        'total_archived': total_archived,
    }

    return render(request, 'notariat/gerer_document.html', context)


@login_required
@user_passes_test(is_secretaire)
def modifier_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    STATUT_CHOICES = Document.STATUT_CHOICES  # Récupérer les choix de statut depuis le modèle
    TYPE_CHOICES = Document.TYPE_CHOICES  # Récupérer les choix de type depuis le modèle
    print(request.POST)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Le document a été modifié avec succès.")
            return redirect('notariat:gerer_document')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = DocumentForm(instance=document)

    demandeurs = User.objects.filter(role='Demandeur')
    return render(request, 'notariat/modifier_document.html', {
        'form': form,
        'document': document,
        'demandeurs': demandeurs,
        'STATUT_CHOICES': STATUT_CHOICES,  # Passez les choix de statut au template
        'TYPE_CHOICES': TYPE_CHOICES  # Passez les choix de type au template
    })


@login_required
@user_passes_test(is_secretaire)
def supprimer_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
        messages.success(request, f'Le document "{document.nom}" a été supprimé avec succès.')
        return redirect('notariat:gerer_document')  # Redirection après suppression

    return render(request, 'notariat/supprimer_document.html', {'document': document})


@login_required
@user_passes_test(is_secretaire)
def archiver_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.statut = Document.STATUT_ARCHIVE  # Mise à jour du statut à "Archivé"
        document.save()
        messages.success(request, f'Le document "{document.nom}" a été archivé avec succès.')
        return redirect('notariat:gerer_document')  # Redirection après archivage

    return render(request, 'notariat/archiver_document.html', {'document': document})


@login_required
@user_passes_test(is_percepteur)
def paiement(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            # Récupérer les données du formulaire
            document_id = request.POST.get('document')
            montant = request.POST.get('montant')
            motif = request.POST.get('motif')
            mode_paiement = request.POST.get('mode_paiement')
            description = request.POST.get('description')

            # Récupérer le document associé
            document = get_object_or_404(Document, id=document_id)
            document.statut = Document.STATUT_PAYE
            document.save()

            # Génération du numéro unique de reçu
            numero_recu = f"REC-{document_id}-{document.recus.count() + 1}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Création du reçu
            recu = Recu.objects.create(
                numero_recu=numero_recu,
                montant=montant,
                motif=motif,
                mode_paiement=mode_paiement,
                description=description,
                document=document,
                utilisateur=request.user  # Utilisateur qui a émis le reçu
            )

            # Message de succès
            messages.success(request, f'Le paiement pour le document "{document.nom}" a été enregistré avec succès.')
            return redirect('notariat:gerer_document')

        except Exception as e:
            # Gestion générique des autres exceptions
            messages.error(request, f"Une erreur est survenue : {str(e)}")

    # Récupérer la liste des documents pour le formulaire
    documents = Document.objects.all()
    return render(request, 'notariat/payement_document.html', {'documents': documents})


@login_required
@user_passes_test(is_percepteur)
def rapport_paiement(request):
    # Récupérer tous les reçus
    recus = Recu.objects.all()

    # Calculer le total des paiements collectés
    total_paiements = recus.aggregate(total=Sum('montant'))['total'] or 0

    # Compter le nombre de documents payés
    documents_payes = recus.count()

    # Compter le nombre de documents non payés
    total_documents = Document.objects.count()
    documents_non_payes = total_documents - documents_payes

    # Préparer les informations à envoyer au template
    context = {
        'total_paiements': total_paiements,
        'documents_payes': documents_payes,
        'documents_non_payes': documents_non_payes,
        'recus': recus
    }

    return render(request, 'notariat/rapport_paiement.html', context)


@login_required
@user_passes_test(is_percepteur)
def rapport_paiement_pdf(request):
    # Récupérer tous les reçus
    recus = Recu.objects.all()

    # Calculer le total des paiements collectés
    total_paiements = recus.aggregate(total=Sum('montant'))['total'] or 0

    # Compter le nombre de documents payés
    documents_payes = recus.count()

    # Compter le nombre de documents non payés
    total_documents = Document.objects.count()
    documents_non_payes = total_documents - documents_payes

    # Préparer les informations à envoyer au template
    context = {
        'total_paiements': total_paiements,
        'documents_payes': documents_payes,
        'documents_non_payes': documents_non_payes,
        'recus': recus
    }

    # Charger le template HTML et convertir en PDF
    template = get_template('notariat/rapport_document_pdf.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_paiement.pdf"'

    # Créer le fichier PDF
    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode('UTF-8')), dest=response, encoding='UTF-8'
    )

    # Si erreur, afficher l'erreur
    if pisa_status.err:
        return HttpResponse(f'Erreur lors de la création du PDF: {pisa_status.err}')
    return response


@login_required
@user_passes_test([is_secretaire, is_notaire])
def voir(request, document_id):
    # Récupération du document à partir de son ID
    document = get_object_or_404(Document, id=document_id)

    context = {
        'document': document,
    }

    return render(request, 'notariat/detail_document.html', context)


@login_required
@user_passes_test(is_secretaire)
def add_demandeur(request):
    if request.method == 'POST':
        form = DemandeurForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le demandeur a été ajouté avec succès !')
            return redirect('notariat:add_demandeur')
        else:
            messages.error(request, 'Une erreur est survenue lors de l’ajout du demandeur.')
    else:
        form = DemandeurForm()

    return render(request, 'notariat/add_demandeur.html', {'form': form})
