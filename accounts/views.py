from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import MyUser as User
from django.contrib import messages
from django.core.mail import send_mail
from booking.models import Restaurants, RestaurantMenu, RestaurantImages, Reserve
from services.generator import Generator
from django.conf import settings
from .forms import RegistrationUserForm
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .forms import RegisterOwnerForm, OwnerUpdateForm, PasswordResetForm, UserForgetEmail

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
            if user.is_restaurant_owner == True:
                return redirect("accounts:registration_owner")
            return redirect("booking:home")
        else:
            messages.error(request, "Kod yalnışdır.")
            return redirect("accounts:activate", slug=slug)
    return render(request, "activate.html", context)


def logout_user(request):
    logout(request)
    return redirect("booking:home")


def password_reset(request, slug):
    user = get_object_or_404(User, slug=slug)
    form = PasswordResetForm()

    if request.method == "POST":
        form = PasswordResetForm(request.POST or None)

        if form.is_valid():
            new_password = form.cleaned_data['password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, "Yeni şifrəniz uğurla təyin edildi")
            login(request, user)
            return redirect("accounts:my_account_user", slug=user.slug)

    context = {
        'form': form
    }

    return render(request, "password-reset.html", context)


def verify_reset(request, slug):
    context = {}
    user = get_object_or_404(User, slug=slug)

    if request.method == "POST":
        code = request.POST.get("code")
        if user.password_reset_code == code:
            return redirect("accounts:password_reset", slug=slug)

    return render(request, "verify-reset.html", context)


def forget_page(request):
    form = UserForgetEmail()
    if request.method == "POST":
        form = UserForgetEmail(request.POST or None)

        if form.is_valid():
            print('salaaam')
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            password_reset_code = Generator.create_reset_code(size=8, model_=User)
            user.password_reset_code = password_reset_code
            user.save()

            subject = "Activation Message"
            message = f"CODE: {password_reset_code}"
            from_mail = settings.EMAIL_HOST_USER
            to_mail = [email]

            send_mail(
                subject, message, from_mail, to_mail, fail_silently=False
            )

            return redirect("accounts:verify_reset", slug=user.slug)
        else:
            print(form.errors)
            form = UserForgetEmail()

    context = {
        'form': form
    }

    return render(request, "forget.html", context)


def registration_user_view(request):
    context = {}
    form = RegistrationUserForm()
    if request.method == "POST":
        form = RegistrationUserForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get("password1"))
            new_user.is_active = False

            # send activation message
            activation_code = Generator.create_activation_code(size=6, model_=User)
            new_user.activation_code = activation_code
            new_user.save()

            subject = "Activation Message"
            message = f"CODE: {activation_code}"
            from_mail = settings.EMAIL_HOST_USER
            to_mail = [new_user.email]

            send_mail(
                subject, message, from_mail, to_mail, fail_silently=False
            )

            return redirect("accounts:activate", slug=new_user.slug)
        else:
            print(form.errors)

    context["form"] = form

    return render(request, "registrationuser.html", context)


def my_account_for_user(request, slug):
    user = get_object_or_404(User, slug=slug)
    restaurant = Restaurants.objects.get(owner=user)
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
        'restaurant': restaurant

    }
    return render(request, "my-account.html", context)


def restaurant_account(request, slug):
    user = get_object_or_404(User, slug=slug)
    restaurant = Restaurants.objects.get(owner=user)
    form = OwnerUpdateForm(instance=restaurant)

    if request.method == "POST":
        print(request.FILES)
        form = OwnerUpdateForm(request.POST, request.FILES or None, instance=restaurant)
        restaurant_images = request.FILES.getlist("rim")
        menu_images = request.FILES.getlist("mim")
        if form.is_valid():
            form.save(commit=False)
            if restaurant_images:
                for rimg in restaurant_images:
                    RestaurantImages.objects.create(
                        restaurant=restaurant,
                        images=rimg
                    )
            if menu_images:
                for mimg in menu_images:
                    RestaurantMenu.objects.create(
                        restaurant=restaurant,
                        menu_images=mimg
                    )
            form.save()

            return redirect("accounts:my_account_user", slug=slug)
    else:
        form = OwnerUpdateForm(instance=restaurant)
    context = {
        "types": CHOICES,
        "restaurant": restaurant,
        'form': form,
        "restaurant_images": restaurant.restaurantimages_set.all(),  # get all the images related to the restaurant
        "menu_images": restaurant.restaurantmenu_set.all(),

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


def delete_image(request, image_id):
    try:
        image = get_object_or_404(RestaurantImages, id=image_id)
        image.delete()
        return JsonResponse({'success': True})
    except RestaurantImages.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image does not exist'})


def delete_menu_image(request, menu_image_id):
    try:
        image = get_object_or_404(RestaurantMenu, id=menu_image_id)
        image.delete()
        return JsonResponse({'success': True})
    except RestaurantMenu.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image does not exist'})


def registration_for_owner(request):
    context = {}
    form = RegisterOwnerForm()

    if request.method == "POST":
        form = RegisterOwnerForm(request.POST, request.FILES or None)
        restaurant_images = request.FILES.getlist("restaurant_images")
        menu_images = request.FILES.getlist("menu_images")
        print(form.errors)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.has_permission = False
            restaurant.owner = request.user
            restaurant.save()
            for restaurant_image in restaurant_images:
                restaurant_images = RestaurantImages.objects.create(
                    restaurant=restaurant,
                    images=restaurant_image
                )
                restaurant_images.save()
            for menu_image in menu_images:
                menu_images = RestaurantMenu.objects.create(
                    restaurant=restaurant,
                    menu_images=menu_image
                )
                menu_images.save()
            return redirect("booking:home")

    context['form'] = form

    return render(request, "registrationowner.html", context)


def registration_person_r(request):
    context = {}
    form = RegistrationUserForm()

    if request.method == "POST":
        form = RegistrationUserForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get("password1"))
            new_user.is_restaurant_owner = True
            new_user.is_active = False

            activation_code = Generator.create_activation_code(size=6, model_=User)
            new_user.activation_code = activation_code
            new_user.save()

            subject = "Activation Message"
            message = f"CODE: {activation_code}"
            from_mail = settings.EMAIL_HOST_USER
            to_mail = [new_user.email]

            send_mail(
                subject, message, from_mail, to_mail, fail_silently=False
            )
            return redirect("accounts:activate", slug=new_user.slug)

    context['form'] = form

    return render(request, "owner-regi.html", context)


def restaurant_reserves(request, slug):
    context = {}
    restaurant = get_object_or_404(Restaurants, slug=slug)
    reserves = Reserve.objects.filter(restaurant=restaurant)
    context['restaurant'] = restaurant
    context['reserves'] = reserves
    return render(request, "restaurant-reserves.html", context)
