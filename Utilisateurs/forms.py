from django import forms
from .models import Utilisateur

class LoginForm(forms.Form):
    username = forms.CharField(label='Nom d’utilisateur')
    # Removed role field
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Nom d’utilisateur', max_length=150)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Téléphone', max_length=15, required=False)
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmer le mot de passe')
    role = forms.ChoiceField(choices=[
        ('gestionnaire_stocks', 'Gestionnaire de Stocks'),
        ('gestionnaire_ventes', 'Gestionnaire de Ventes'),
    ], label='Rôle')
    
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'role', 'phone', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.") 
