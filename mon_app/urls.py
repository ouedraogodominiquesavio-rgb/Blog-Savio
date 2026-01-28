from django.urls import path
from . import views
from .views import accueil

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('formations/', views.liste_formations, name='liste_formations'),
    path('sessions/', views.liste_sessions, name='liste_sessions'),
    path('inscription/', views.inscrire_session, name='inscrire_session'),
    path('produits/', views.liste_produits, name='liste_produits'),
    path('panier/', views.panier, name='panier'),
    path('ajouter_au_panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('contact/', views.contact, name='contact'),
    path('paiement/initier/', views.initier_paiement, name='initier_paiement'),
    path('', accueil, name='accueil'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('inscription/success/', views.inscription_success, name='inscription_success'), 
    path('formation/', views.liste_formations, name='liste_formations_alias'),

    

    
]
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import SessionFormation, Inscription

@login_required
def inscrire_session(request):
    """
    Permet à l'utilisateur de s'inscrire à une ou plusieurs sessions et envoie un email.
    """
    if request.method == 'POST':
        # Infos personnelles
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        profession = request.POST.get('profession')
        niveau = request.POST.get('niveau')

        # Sessions sélectionnées
        sessions_id = request.POST.getlist('sessions')
        sessions_inscrites = []

        for session_id in sessions_id:
            session = get_object_or_404(SessionFormation, id=session_id)
            if session.places_disponibles() > 0:
                if not Inscription.objects.filter(client=request.user, session=session).exists():
                    Inscription.objects.create(
                        client=request.user,
                        session=session,
                        nom=nom,
                        prenom=prenom,
                        sexe=sexe,
                        profession=profession,
                        niveau=niveau
                    )
                    session.places_reservees += 1
                    session.save()
                    sessions_inscrites.append(session.cours.titre)
                else:
                    messages.warning(request, f"Déjà inscrit à {session.cours.titre}")
            else:
                messages.error(request, f"Plus de places pour {session.cours.titre}")

        # Envoi de l'email
        if sessions_inscrites:
            sujet = f"Nouvelle inscription de {prenom} {nom}"
            contenu = f"""
Nom: {nom}
Prénom: {prenom}
Sexe: {sexe}
Profession: {profession}
Niveau: {niveau}
Email utilisateur: {request.user.email}

Sessions choisies:
- {"\n- ".join(sessions_inscrites)}
            """
            send_mail(
                sujet,
                contenu,
                settings.DEFAULT_FROM_EMAIL,
                ['ouedraogodominiquesavio@gmail.com'],
                fail_silently=False
            )

        messages.success(request, "Inscription enregistrée et email envoyé !")
        return redirect('liste_sessions')

    sessions = SessionFormation.objects.all().order_by('date_debut')
    return render(request, 'mon_app/inscription.html', {'sessions': sessions})
