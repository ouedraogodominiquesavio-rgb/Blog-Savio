from django.contrib import admin
from .models import Article, Cours, SessionFormation, Inscription, Produit, Commande, ItemCommande, Paiement, Message



# ===== BLOG =====
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_pub')
    search_fields = ('titre', 'contenu')
    list_filter = ('date_pub',)

# ===== FORMATIONS =====
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix')
    search_fields = ('titre', 'description')
    list_filter = ('prix',)

# ===== SESSIONS =====
@admin.register(SessionFormation)
class SessionFormationAdmin(admin.ModelAdmin):
    list_display = ('cours', 'date_debut', 'date_fin', 'places_totales', 'places_reservees', 'places_disponibles')
    list_filter = ('cours', 'date_debut')

# ===== INSCRIPTIONS =====
@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'session', 'date_inscription')
    list_filter = ('session',)

# ===== BOUTIQUE =====
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix')
    search_fields = ('nom', 'description')
    list_filter = ('prix',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('client', 'date_commande', 'paye')
    list_filter = ('paye', 'date_commande')

@admin.register(ItemCommande)
class ItemCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite')

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('commande', 'montant', 'statut', 'date')

# ===== CONTACT =====
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'sexe', 'profession', 'email', 'date_envoye')
    search_fields = ('nom', 'prenom', 'email')
