from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.forms import TransactionForm, RegistrationForm, LoginForm
from accounts.models import TransactionModel


def homepage(request):
    return render(request, 'home.html')

def transaction(request):
    transaction_form = TransactionForm(request.POST or None)

    if transaction_form.is_valid():
        if transaction_form.cleaned_data['credit']:
            transaction_form.cleaned_data['amount'] += previous_balance(request)
        else:
            transaction_form.cleaned_data['amount'] -= previous_balance(request) + transaction_form.cleaned_data['amount']
        
        transaction_form.save()
        return redirect('/transaction/')

    return render(request, 'transaction_form.html', {'form': transaction_form})

def previous_balance(request):
    balance = TransactionModel.objects.filter(
        username = request.user
    )
    
    if balance:
        return balance[-1]['amount']
    return 0

def get_categorized_data(request):
    data = TransactionModel.objects.filter(
        username = request.user
    )

    categories = list(set([entry['category'] for entry in data]))

    categorized_data = []
    for category in categories:
        category_data = []
        for entry in data:
            if entry['category'] == category:
                category_data.append(entry)
        categorized_data.append(category_data)

    return categorized_data

def registration(request):
    registration_form = RegistrationForm(request.POST or None)

    if registration_form.is_valid():
        username = registration_form.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists.')
            return redirect('/registration/')
        
        user = registration_form.save(commit=False)
        user.set_password(registration_form.cleaned_data['password'])
        user.save()

        messages.info(request, 'Account Created.')
        return redirect('home')
        
    return render(request, 'register.html', {'form': registration_form})

def login_user(request):
    login_form = LoginForm(request.POST or None)

    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Username does not exists.')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, 'Enter correct password')
            return redirect('/login/')
        
        login(request, user)
        return redirect('home')

    return render(request, 'login.html', {'form': login_form})

def logout_user(request):
    logout(request)
    return redirect('home')
