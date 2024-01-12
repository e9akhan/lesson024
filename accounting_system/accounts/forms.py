"""
    Module Name :- forms
    Classes :- TransactionForm, RegistrationForm, LoginForm
"""

from django import forms
from django.contrib.auth.models import User
from accounts.models import TransactionModel


class TransactionForm(forms.ModelForm):
    """
    Form to make transaction.
    """

    credit = forms.BooleanField(required=False)

    class Meta:
        """
        Meta class for Transaction Form.
        """

        model = TransactionModel
        exclude = ["date", "user", "balance"]

        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "amount": forms.TextInput(attrs={"class": "form-control"}),
            "mode_of_payment": forms.Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True, user=None, balance=0):
        """
        Save the form data into database.
        """
        instance = super().save(commit=False)

        if not instance.user_id:
            instance.user = user

        if not instance.balance:
            instance.balance = balance

        if commit:
            instance.save()

        return instance


class RegistrationForm(forms.ModelForm):
    """
    Form to register user.
    """

    class Meta:
        """
        Meta class for Registration form.
        """

        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    """
    Form for use login.
    """

    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    username.widget.attrs.update({"class": "form-control"})
    password.widget.attrs.update({"class": "form-control"})
