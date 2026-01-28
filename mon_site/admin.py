from django.contrib import admin
from .models import Article, Cours, SessionFormation, Inscription, Produit, Commande, ItemCommande, Paiement, Message

# ===== BLOG =====
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_pub')
    search_fields = ('titre', 'contenu')
    list_filter = ('date_pub',)


# ===== FORMATION =====
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix')
    search_fields = ('titre', 'description')
    list_filter = ('prix',)


@admin.register(SessionFormation)
class SessionFormationAdmin(admin.ModelAdmin):
    list_display = ('cours', 'date_debut', 'date_fin', 'places_totales', 'places_reservees', 'places_disponibles')
    list_filter = ('cours', 'date_debut')
    search_fields = ('cours__titre',)

    def places_disponibles(self, obj):
        return obj.places_disponibles()
    places_disponibles.short_description = "Places disponibles"


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'session', 'client', 'sexe', 'profession', 'niveau', 'date_inscription')
    search_fields = ('nom', 'prenom', 'profession', 'niveau', 'session__cours__titre', 'client__username')
    list_filter = ('sexe', 'profession', 'niveau', 'session')


# ===== BOUTIQUE =====
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix')
    search_fields = ('nom', 'description')


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_commande', 'paye', 'reference_payment', 'total_commande')
    list_filter = ('paye', 'date_commande')
    search_fields = ('client__username', 'reference_payment')

    def total_commande(self, obj):
        return obj.total()
    total_commande.short_description = "Total commande"


@admin.register(ItemCommande)
class ItemCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite', 'total_item')
    search_fields = ('produit__nom', 'commande__client__username')

    def total_item(self, obj):
        return obj.total()
    total_item.short_description = "Total"


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('commande', 'montant', 'statut', 'reference', 'date')
    list_filter = ('statut', 'date')
    search_fields = ('commande__client__username', 'reference')


# ===== CONTACT =====
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'sexe', 'profession', 'email', 'date_envoye')
    search_fields = ('prenom', 'nom', 'profession', 'email')
    list_filter = ('sexe', 'profession')
