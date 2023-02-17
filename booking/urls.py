from django.urls import path
from .views import home_view, about_view, list_view, blog_view, contact_view


app_name = "booking"
urlpatterns = [
    path('home', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('restaurants/', list_view, name='list'),
    path('blog/', blog_view, name='blog'),
    path('contact/', contact_view, name='contact'),
]