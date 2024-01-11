"""
    Module Name :- forms
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import TransactionModel

class TransactionForm(forms.ModelForm):
    credit = forms.BooleanField()

    class Meta:
        model = TransactionModel
        exclude = ['date', 'username']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_of_payment': forms.Select(attrs={'class': 'form-control'})
        }

    def save(self):
        data = self.cleaned_data

        transaction = TransactionModel.objects.filter(
            username = self.kwargs.request.user,
            category = data['category'],
            description = data['description'],
            amount = data['amount'],
            mode_of_payment = data['mode_of_payment']
        )
        transaction.save()

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
