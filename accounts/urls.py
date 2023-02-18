from django.urls import path
from .views import login_user_view, registration_user_view, forget_password_user, login_for_owner, forget_password_owner

app_name = 'accounts'
urlpatterns = [
    path("login/user/", login_user_view, name='login_user'),
    path("registration/user/", registration_user_view, name='registration_user'),
    path("forgetpassword/user/", forget_password_user, name='forgetuser'),
    path("login/owner/", login_for_owner, name='login_owner'),
    path("registration/owner/", registration_user_view, name='registration_owner'),
    path("forgetpassword/owner/", forget_password_owner, name='forgetowner')
]