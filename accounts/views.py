from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

def login_user_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("booking:home")
        else:
            return render(request, "loginuser.html", {"message": "email yaxud parol yalnisdir"})

    context = {

    }

    return render(request, "loginuser.html", context)


def registration_user_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        birthday = request.POST.get("birthday")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("agpassword")
        number = request.POST.get("number")

        print(email)

        if password == re_password:
            if User.objects.filter(username=username).exists():
                return render(request, "registrationuser.html", {"error": "basqa bir user bu adla qeydiyyatdan kecib"})

            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "registrationuser.html",
                                  {"error": "basqa bir user bu emaille qeydiyyatdan kecib"})
                else:
                    user = User.objects.create_user(
                        username=username,
                        number=number,
                        birthday=birthday,
                        gender=gender,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password
                    )
                    user.save()
                    return redirect("accounts:login")


        else:
            return render(request, "registrationuser.html", {"error":"parollar uygunlasmir"})

    context = {

    }
    return render(request, "registrationuser.html", context)


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
    context = {

    }

    return render(request, "registrationowner.html", context)


def forget_password_owner(request):
    context = {

    }

    return render(request, "forget-password-owner.html", context)
