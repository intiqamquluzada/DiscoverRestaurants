from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import MyUser as User
from django.contrib import messages
from booking.models import Countries
from django.core.mail import send_mail
from booking.models import Restaurants, RestaurantMenu, RestaurantImages
from services.generator import Generator
from django.conf import settings
from django.http import HttpResponseServerError
from django.contrib.auth.hashers import check_password
from booking.models import RestaurantImages

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

        user = User.objects.create(
            name=request.POST.get("firstname"),
            surname=request.POST.get("lastname"),
            email=request.POST.get("email"),
            gender=request.POST.get("gender"),
            phone=request.POST.get("number"),
            is_active=False,
        )
        user.set_password(request.POST.get("password"))
        user.save()

        # send activation part
        activation_code = Generator.create_activation_code(size=6, model_=User)
        user.activation_code = activation_code
        user.save()
        subject = "Activation message"
        message = f"Recovery code: {activation_code}"
        from_mail = settings.EMAIL_HOST_USER
        to_mail = [user.email]

        try:
            send_mail(
                subject, message, from_mail, to_mail, fail_silently=False
            )
        except Exception as e:
            print(e)
            return HttpResponseServerError("Failed to send activation email.")

        return redirect("accounts:activate", slug=user.slug)

    context = {

    }
    return render(request, "registrationuser.html", context)


def activate_user_view(request, slug):
    context = {}
    user = get_object_or_404(User, slug=slug)

    if request.method == "POST":
        code = request.POST.get("code", None)

        if code == user.activation_code:
            user.is_active = True
            user.activation_code = None
            user.save()
            login(request, user)
            return redirect("booking:home")
        else:
            messages.error(request, "Kod yalnışdır.")
            return redirect("accounts:activate", slug=slug)
    return render(request, "activate.html", context)


def logout_user(request):
    logout(request)
    return redirect("booking:home")


def forget_password_user(request):
    context = {

    }

    return render(request, "forget-password.html", context)


def my_account_for_user(request, slug):
    user = get_object_or_404(User, slug=slug)
    if user.pp:
        if request.method == "POST" and ('form2_submit' in request.POST):
            user.pp.delete()
            print(user.pp.delete())
            user.save()
    else:
        if request.method == "POST" and request.FILES and ('form1_submit' in request.POST):
            print(request.FILES)
            pp_photo = request.FILES.get("pp_photo")
            user.pp = pp_photo
            user.save()
    if request.method == "POST" and ('form3_submit' in request.POST):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        phone = request.POST.get("phone")
        old_pass = request.POST.get("old_pass")
        new_pass_1 = request.POST.get("new_pass1")
        new_pass_2 = request.POST.get("new_pass2")
        if name:
            user.name = name
        if surname:
            user.surname = surname
        if phone:
            user.phone = phone
        user.save()
        if new_pass_1 or new_pass_2:
            if check_password(old_pass, user.password):
                if new_pass_2 == new_pass_1:
                    user.set_password(new_pass_1)
                    user.save()
                    login(request, user)
                    return redirect("accounts:my_account_user", slug=slug)
                else:
                    messages.error(request, 'Şifrələr uyğun deyil')
            else:
                messages.error(request, "Köhnə şifrəniz yalnışdır")

    context = {

    }
    return render(request, "my-account.html", context)


def restaurant_account(request, slug):
    user = get_object_or_404(User, slug=slug)
    restaurant = Restaurants.objects.filter(owner=user)
    countries = Countries.objects.all()
    if request.method == "POST" and ("total" in request.POST) and request.FILES:
        print(request.POST and request.FILES)

    context = {
        "types": CHOICES,
        "restaurant": restaurant,
        'countries': countries,

    }
    return render(request, "faqs.html", context)


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
    countries = Countries.objects.all()
    print(countries)

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
            user.set_password(pass_1)
            user.save()
            restaurant = Restaurants.objects.create(

                owner=user,
                name=request.POST.get("rname"),
                country_of_restaurant=Countries.objects.get(name=request.POST.get("rcountry")),
                city=request.POST.get("rcity"),
                type_r=request.POST.get("rtype"),
                number=request.POST.get("rphone"),
                location=request.POST.get("radres"),
                available_seats=request.POST.get("rcount"),
                description=request.POST.get("rdescription"),
            )
            restaurant.save()
            images = request.FILES.getlist("rimage")
            for img in images:
                restaurant_images = RestaurantImages.objects.create(
                    restaurant=restaurant,
                    images=img

                )
                restaurant_images.save()
            menu_images = request.FILES.getlist("rmenu")
            for mimg in menu_images:
                restaurant_menu = RestaurantMenu.objects.create(
                    restaurant=restaurant,
                    menu_images=mimg
                )
            restaurant_menu.save()

            return redirect("accounts:login_owner")
        else:
            context['info'] = "Parollar uyğun deyil"

    context['types'] = CHOICES
    context['countries'] = countries

    return render(request, "registrationowner.html", context)


def forget_password_owner(request):
    context = {

    }

    return render(request, "forget-password-owner.html", context)







