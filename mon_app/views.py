import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Article, Cours, SessionFormation, Inscription,
    Produit, Commande, ItemCommande, Paiement, Message
)
from .forms import InscriptionForm

# ===== ACCUEIL =====
def accueil(request):
    articles = Article.objects.all().order_by('-date_pub')
    cours = Cours.objects.all()
    produits = Produit.objects.all()
    return render(request, 'accueil.html', {
        'articles': articles,
        'cours': cours,
        'produits': produits
    })

# ===== FORMATIONS =====
def liste_formations(request):
    cours = Cours.objects.all()
    return render(request, 'formation.html', {'cours': cours})

def liste_sessions(request):
    sessions = SessionFormation.objects.all().order_by('date_debut')
    return render(request, 'sessions.html', {'sessions': sessions})

@login_required
def inscrire_session(request):
    if request.method == 'POST':
        sessions_id = request.POST.getlist('sessions')
        for session_id in sessions_id:
            session = get_object_or_404(SessionFormation, id=session_id)
            if session.places_disponibles() > 0:
                if not Inscription.objects.filter(client=request.user, session=session).exists():
                    Inscription.objects.create(client=request.user, session=session)
                    session.places_reservees += 1
                    session.save()
                    messages.success(request, f"Inscription réussie pour {session.cours.titre}")
                else:
                    messages.warning(request, f"Vous êtes déjà inscrit à {session.cours.titre}")
            else:
                messages.error(request, f"Plus de places disponibles pour {session.cours.titre}")
        return redirect('liste_sessions')
    sessions = SessionFormation.objects.all().order_by('date_debut')
    return render(request, 'inscription.html', {'sessions': sessions})

# ===== BOUTIQUE =====
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'produits.html', {'produits': produits})

@login_required
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    commande, created = Commande.objects.get_or_create(client=request.user, paye=False)
    item, created = ItemCommande.objects.get_or_create(commande=commande, produit=produit)
    item.quantite += 1
    item.save()
    messages.success(request, f"{produit.nom} ajouté au panier !")
    return redirect('liste_produits')

@login_required
def panier(request):
    commande = Commande.objects.filter(client=request.user, paye=False).first()
    return render(request, 'panier.html', {'commande': commande})

# ===== CONTACT =====
def contact(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        profession = request.POST.get('profession')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        Message.objects.create(
            nom=nom,
            prenom=prenom,
            sexe=sexe,
            profession=profession,
            email=email,
            message=message_text
        )

        send_mail(
            subject=f"Nouveau message de {prenom} {nom}",
            message=f"Nom: {nom}\nPrénom: {prenom}\nSexe: {sexe}\nProfession: {profession}\nEmail: {email}\n\nMessage:\n{message_text}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['ouedraogodominiquesavio@gmail.com'],
            fail_silently=False
        )
        messages.success(request, "Votre message a été envoyé avec succès !")
        return redirect('accueil')

    return render(request, 'contact.html')

# ===== INSCRIPTION FORMATION =====
def inscription_view(request):
    form = InscriptionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        inscription = form.save(commit=False)
        if request.user.is_authenticated:
            inscription.client = request.user
        inscription.save()
        send_mail(
            subject=f"Nouveau client inscrit : {inscription.prenom} {inscription.nom}",
            message=f"Nom: {inscription.nom}\nPrénom: {inscription.prenom}\nSexe: {inscription.sexe}\nProfession: {inscription.profession}\nNiveau: {inscription.niveau}\nSession: {inscription.session}\nEmail utilisateur: {inscription.client.email if inscription.client else 'Non connecté'}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['ouedraogodominiquesavio@gmail.com'],
        )
    
def inscription_success(request):
    return render(request, 'inscription_success.html')


# ===== PAIEMENT =====
@login_required
def initier_paiement(request):
    commande = Commande.objects.filter(client=request.user, paye=False).first()
    if not commande:
        messages.error(request, "Vous n'avez pas de commande en attente.")
        return redirect('liste_produits')

    paiement, created = Paiement.objects.get_or_create(commande=commande, montant=commande.total())
    paiement.generer_otp()  # Génère l'OTP pour la validation
    messages.success(request, f"Paiement initié avec référence {paiement.reference or paiement.id} et OTP {paiement.otp}")
    return redirect('panier')

@login_required
def valider_otp(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id, commande__client=request.user)
    if request.method == 'POST':
        otp_saisi = request.POST.get('otp')
        if otp_saisi == paiement.otp:
            paiement.statut = 'Réussi'
            paiement.save()
            paiement.commande.paye = True
            paiement.commande.save()
            messages.success(request, "Paiement validé avec succès !")
            return redirect('accueil')
        else:
            messages.error(request, "OTP incorrect. Veuillez réessayer.")
    return render(request, 'valider_otp.html', {'paiement': paiement})
