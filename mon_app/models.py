from django.db import models
from django.contrib.auth.models import User
import random

# ===== BLOG =====
class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


# ===== FORMATION =====
class Cours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='formations/', blank=True, null=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return self.titre


class SessionFormation(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    places_totales = models.PositiveIntegerField()
    places_reservees = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.cours.titre} du {self.date_debut.strftime('%d/%m/%Y')}"

    def places_disponibles(self):
        return self.places_totales - self.places_reservees


# ===== INSCRIPTION =====
class Inscription(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionFormation, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    profession = models.CharField(max_length=150)
    niveau = models.CharField(max_length=200, help_text="Exemple : Débutant, Intermédiaire, Avancé ou déjà suivi un cours")
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'session')

    def __str__(self):
        return f"{self.nom} {self.prenom} -> {self.session.cours.titre}"


# ===== BOUTIQUE =====
class Produit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/')

    def __str__(self):
        return self.nom


class Commande(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    paye = models.BooleanField(default=False)
    reference_payment = models.CharField(max_length=100, blank=True, null=True)

    def total(self):
        return sum(item.total() for item in self.items.all())

    def __str__(self):
        return f"Commande {self.id} de {self.client.username}"


class ItemCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='items', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def total(self):
        return self.produit.prix * self.quantite

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"


class Paiement(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, default='En attente')  # En attente, Réussi, Échoué
    reference = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)  # OTP pour validation
    date = models.DateTimeField(auto_now_add=True)

    def generer_otp(self):
        """Génère un OTP à 6 chiffres"""
        self.otp = f"{random.randint(100000, 999999)}"
        self.save()
        return self.otp

    def __str__(self):
        return f"Paiement {self.reference} - {self.statut}"


# ===== CONTACT =====
class Message(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    profession = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    date_envoye = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.sexe}) - {self.profession}"
