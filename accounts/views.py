from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model



def login_user_view(request):


    context = {

    }

    return render(request, "loginuser.html", context)


def registration_user_view(request):



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
