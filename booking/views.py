from django.shortcuts import render
from .models import Restaurants, CooperationCompanies, Countries, Cities
import requests
import json

api_key = '5117dbe9476548a6834433afd9b63554'

api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + api_key


def get_ip_geolocation_data(ip_address):
    # not using the incoming IP address for testing

    print(ip_address)

    response = requests.get(api_url)

    return response.content


def home_view(request):
    companies_corporation = CooperationCompanies.objects.all()
    rate = Restaurants.objects.all().values_list('rating', flat=True)
    popular_restaurants = Restaurants.objects.filter(rating=5)
    countries_list = Countries.objects.all()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:

        ip = x_forwarded_for.split(',')[0]

    else:

        ip = request.META.get('REMOTE_ADDR')

    geolocation_json = get_ip_geolocation_data(ip)

    geolocation_data = json.loads(geolocation_json)

    country = geolocation_data['country']

    region = geolocation_data['region']

    cont = Countries.objects.filter(name=str(country)).values('slug')

    print(cont)

    result = Restaurants.objects.filter(id__lte=8)

    city = Cities.objects.filter(country__slug__in=cont)

    context = {
        'countries_list': countries_list,
        'city': city,
        'country': country,
        'region': region,
        'companies': companies_corporation,
        'popular': popular_restaurants,

        'restaurants': result
    }
    return render(request, "index.html", context)


def about_view(request):
    context = {

    }

    return render(request, "privacy-policy.html", context)


def list_view(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:

        ip = x_forwarded_for.split(',')[0]

    else:

        ip = request.META.get('REMOTE_ADDR')

    geolocation_json = get_ip_geolocation_data(ip)

    geolocation_data = json.loads(geolocation_json)

    country = geolocation_data['country']

    region = geolocation_data['region']

    cont = Countries.objects.filter(name=str(country)).values('slug')

    result = Restaurants.objects.filter(country_of_restaurant__slug__in=cont)

    context = {
        'result': result,
        'country': country,
        'region': region,

    }
    return render(request, 'list.html', context)


def blog_view(request):
    context = {

    }

    return render(request, "blog.html", context)


def contact_view(request):
    context = {

    }

    return render(request, "contact.html", context)
