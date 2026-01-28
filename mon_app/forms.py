from django import forms
from .models import Inscription, Message

# Formulaire d'inscription à une formation
class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['session', 'nom', 'prenom', 'sexe', 'profession', 'niveau']
        widgets = {
            'session': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulaire pour le contact
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['nom', 'prenom', 'sexe', 'profession', 'email', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
