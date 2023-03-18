from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import MyUser as User
from django.contrib import messages
from booking.models import Countries, Cities
from django.db.models import Prefetch
from booking.models import Restaurants, RestaurantMenu, RestaurantImages


def login_user_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_restaurant_owner == False:
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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_restaurant_owner == True:
            login(request, user)
            return redirect('booking:home')
        else:
            messages.error(request, 'Invalid username or password')

    context = {

    }

    return render(request, "loginowner.html", context)


def registration_for_owner(request):
    context = {}
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
    gg = Countries.objects.all().values_list("name", flat=True)
    print(gg)
    countries = Countries.objects.prefetch_related(Prefetch('cities', queryset=Cities.objects.order_by('name')))

    pass_1 = request.POST.get("ownerpass1")
    pass_2 = request.POST.get("ownerpass2")
    print(request.POST)
    if request.method == "POST":
        if pass_2 == pass_1:
            user = User.objects.create(
                name=request.POST.get("ownername"),
                surname='Sahibkar',
                email=request.POST.get("ownermail"),
                phone=request.POST.get("ownerphone"),
                is_active=False,
                is_restaurant_owner=True,
            )
            restaurant = Restaurants.objects.create(

                owner=user,
                name=request.POST.get("rname"),
                country_of_restaurant=request.POST.get("rcountry"),
                city=request.POST.get("rcity"),
                type_r=request.POST.get("rtype"),
                number=request.POST.get("rphone"),
                location=request.POST.get("radres"),
                available_seats=request.POST.get("rcount"),
                description=request.POST.get("rdescription"),
            )
            images = request.FILES.getlist("rimage")
            for img in images:
                restaurant_images = RestaurantImages.objects.create(
                    restaurant=restaurant,
                    images=img


                )
            menu_images = request.FILES.getlist("rmenu")
            for mimg in menu_images:
                restaurant_menu = RestaurantMenu.objects.create(
                    restaurant=restaurant,
                    menu_images=mimg
                )

            user.set_password(pass_1)
            user.save()
            return redirect("accounts:login_owner")
        else:
            context['info'] = "Parollar uyğun deyil"

    context['types'] = CHOICES
    context['countries'] = countries
    context['gg'] = gg

    return render(request, "registrationowner.html", context)


def forget_password_owner(request):
    context = {

    }

    return render(request, "forget-password-owner.html", context)
