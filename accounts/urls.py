from django.urls import path
from .views import (login_user_view, registration_user_view,
                    registration_for_owner, forget_page,
                    login_for_owner, logout_user, password_reset,
                    activate_user_view, my_account_for_user, restaurant_account,
                    delete_image, registration_person_r, delete_menu_image, verify_reset)

app_name = 'accounts'

urlpatterns = [
    path("login/user/", login_user_view, name='login_user'),
    path("registration/user/", registration_user_view, name='registration_user'),
    path("login/owner/", login_for_owner, name='login_owner'),
    path("registration/owner/", registration_for_owner, name='registration_owner'),
    path("logout/user/", logout_user, name='logout_user'),
    path("activate/<slug>/", activate_user_view, name='activate'),
    path("verify-reset/<slug>/", verify_reset, name='verify_reset'),
    path("password-reset/<slug>/", password_reset, name='password_reset'),
    path("my-account-user/<slug>/", my_account_for_user, name='my_account_user'),
    path("restaurant-account/<slug>/", restaurant_account, name='restaurantchanging'),
    path('delete-image/<image_id>/', delete_image, name='delete_image'),
    path('delete-menu-image/<menu_image_id>/', delete_menu_image, name='delete_menu_image'),
    path('owner-regi/', registration_person_r, name='owner_reg'),
    path("forget/", forget_page, name='forget')

]
