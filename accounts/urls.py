from django.urls import path
from .views import (login_user_view, registration_user_view,
                    forget_password_user, registration_for_owner,
                    login_for_owner, forget_password_owner, logout_user,
                    activate_user_view, my_account_for_user, restaurant_account, delete_image)

app_name = 'accounts'
urlpatterns = [
    path("login/user/", login_user_view, name='login_user'),
    path("registration/user/", registration_user_view, name='registration_user'),
    path("forgetpassword/user/", forget_password_user, name='forgetuser'),
    path("login/owner/", login_for_owner, name='login_owner'),
    path("registration/owner/", registration_for_owner, name='registration_owner'),
    path("forgetpassword/owner/", forget_password_owner, name='forgetowner'),
    path("logout/user/", logout_user, name='logout_user'),
    path("activate/<slug>/", activate_user_view, name='activate'),
    path("my-account-user/<slug>/", my_account_for_user, name='my_account_user'),
    path("restaurant-account/<slug>/", restaurant_account, name='restaurantchanging'),
    path('delete-image/', delete_image, name='delete-image'),

]
