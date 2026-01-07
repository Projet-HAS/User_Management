
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserCreateForm(forms.Form):
    
    # Identité
    first_name = forms.CharField(label=_("Prénom"), max_length=150, required=True)
    last_name = forms.CharField(label=_("Nom"), max_length=150, required=True)

    # Identifiant
    email = forms.EmailField(label=_("Email"), required=True)

    # Mot de passe
    password1 = forms.CharField(label=_("Mot de passe"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_("Confirmation du mot de passe"), widget=forms.PasswordInput, required=True)
    
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un utilisateur avec cet email existe déjà.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", _("Les mots de passe ne correspondent pas."))
        # Valide selon les règles Django (force, longueur, etc.)
        if p1:
            try:
                validate_password(p1)
            except ValidationError as e:
                self.add_error("password1", e)
        return cleaned

    def save(self):
        """
        Crée l'utilisateur et ajoute au groupe 'Administrator'
        Retourne l'instance User créée.
        """
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        first_name = self.cleaned_data["first_name"].strip()
        last_name = self.cleaned_data["last_name"].strip()

        user = User.objects.create_user(email=email, password=password)
        
        # Identité
        user.first_name = first_name
        user.last_name = last_name

        user.save()

        group, _ = Group.objects.get_or_create(name="Administrator")
        user.groups.add(group)

        return user
