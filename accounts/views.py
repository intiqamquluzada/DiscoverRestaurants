from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import MyUser as User
from django.contrib import messages
from booking.models import Countries, Cities


def login_user_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('booking:home')
        else:
            messages.error(request, 'Invalid username or password')

    context = {

    }

    return render(request, "loginuser.html", context)


def registration_user_view(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.create(
            name=request.POST.get("firstname"),
            surname=request.POST.get("lastname"),
            email=request.POST.get("email"),
            gender=request.POST.get("gender"),
            phone=request.POST.get("number")
        )
        user.set_password(request.POST.get("password"))
        user.save()
        return redirect("accounts:login_user")

    context = {

    }
    return render(request, "registrationuser.html", context)


def logout_user(request):
    logout(request)
    return redirect("booking:home")


def forget_password_user(request):
    context = {

    }

    return render(request, "forget-password.html", context)


def my_account_for_user(request):
    context = {

    }
    return render(request, "my-account.html", context)


def login_for_owner(request):



    context = {

    }

    return render(request, "loginowner.html", context)


def registration_for_owner(request):
    CHOICES = (
        ('Fast-food', 'Fast-food'),
        ('Milli', 'Milli'),
        ('Ailəvi', 'Ailəvi'),
        ('Business-lunch', 'Business-lunch'),
        ('Şirniyyat', 'Şirniyyat'),
        ('Vegetarian', 'Vegetarian'),
        ('Özünə xidmət', 'Özünə xidmət'),
        ('Klub', 'Klub'),
    )

    countries = Countries.objects.all().values_list("name", flat=True)
    cities = Cities.objects.all().values_list("name", flat=True)
    print(cities, countries)
    print(55555)


    if request.method == "POST":
        print(request.POST)


    context = {

        'types': CHOICES,
        'countries': countries,
        'cities': cities,

    }

    return render(request, "registrationowner.html", context)


def forget_password_owner(request):
    context = {

    }

    return render(request, "forget-password-owner.html", context)
