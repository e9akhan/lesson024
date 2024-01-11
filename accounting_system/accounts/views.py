"""
    Module nme :- views
    Method(s) :- homepage(), transaction(), previous_balance(), registration(), login_user(),
    logout_user(), transaction_history()
"""

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.forms import TransactionForm, RegistrationForm, LoginForm
from accounts.models import TransactionModel


def homepage(request):
    """
    Returns homepage of website.
    """
    return render(request, "home.html")


def transaction(request):
    """
    Make the transactions.
    """
    transaction_form = TransactionForm(request.POST or None)

    if transaction_form.is_valid():
        credit = transaction_form.cleaned_data["credit"]

        if credit:
            balance = (
                previous_balance(request) + transaction_form.cleaned_data["amount"]
            )
        else:
            balance = (
                previous_balance(request) - transaction_form.cleaned_data["amount"]
            )

        if balance < 0:
            messages.info(request, "Not sufficient amount")
            return redirect("/transaction/")

        transaction_form.save(user=request.user, balance=balance)

        if credit:
            messages.info(request, "Amount Successfully credited.")
        else:
            messages.info(request, "Amount Successfully debited.")

        return redirect("/transaction/")

    return render(request, "transaction_form.html", {"form": transaction_form})


def previous_balance(request):
    """
    Extract previous balance.
    """
    balance = list(TransactionModel.objects.filter(user=request.user))

    if balance:
        return balance[-1].balance
    return 0


def registration(request):
    """
    Register users.
    """
    registration_form = RegistrationForm(request.POST or None)

    if registration_form.is_valid():
        username = registration_form.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists.")
            return redirect("/registration/")

        user = registration_form.save(commit=False)
        user.set_password(registration_form.cleaned_data["password"])
        user.save()

        messages.info(request, "Account Created.")
        return redirect("/login/")

    return render(request, "register.html", {"form": registration_form})


def login_user(request):
    """
    Login the user.
    """
    login_form = LoginForm(request.POST or None)

    if login_form.is_valid():
        username = login_form.cleaned_data["username"]
        password = login_form.cleaned_data["password"]

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Username does not exists.")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Enter correct password")
            return redirect("/login/")

        login(request, user)
        return redirect("home")

    return render(request, "login.html", {"form": login_form})


def logout_user(request):
    """
    Logout user.
    """
    logout(request)
    return redirect("home")


def transaction_history(request):
    """
    Displays the transaction history.
    """
    transactions = TransactionModel.objects.filter(user=request.user)
    return render(request, "transaction_history.html", {"data": transactions})
