from django.shortcuts import render, redirect
from django.db.models import F
from .models import Restaurants, CooperationCompanies, Countries, Comment, Likes, Rating, Reserve
import requests
import json
from django.contrib.auth import get_user_model
from accounts.models import MyUser
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm, ReserveForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

api_key = "5117dbe9476548a6834433afd9b63554"

api_url = "https://ipgeolocation.abstractapi.com/v1/?api_key=" + api_key


def get_ip_geolocation_data(ip_address):
    # not using the incoming IP address for testing

    print(ip_address)

    response = requests.get(api_url)

    return response.content


User = MyUser()



def home_view(request):
    companies_corporation = CooperationCompanies.objects.all()

    popular_restaurants = Restaurants.objects.filter(rating=5)
    countries_list = Countries.objects.all()

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:

        ip = x_forwarded_for.split(",")[0]

    else:

        ip = request.META.get("REMOTE_ADDR")

    geolocation_json = get_ip_geolocation_data(ip)

    geolocation_data = json.loads(geolocation_json)

    country = geolocation_data["country"]

    region = geolocation_data["region"]

    result = Restaurants.objects.all()

    search = request.GET.get('q', None)

    if search:
        result = Restaurants.objects.filter(country_of_restaurant__name__icontains=search)

    if result.count() == 0:
        message = "Sənin axtarışına uyğun nəticə tapılmadı"
        print(message)
    else:
        message = ""

    paginator = Paginator(result, 4)
    page = request.GET.get('page', 1)
    p = paginator.get_page(page)
    total = Restaurants.objects.all()
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    context = {
        'restaurants': result,
        'total': total,
        'p': p,
        'search': search,
        'countries_list': countries_list,
        'paginator': paginator,
        'message': message,
        'country': country,
        'region': region,
        'companies': companies_corporation,
        'popular': popular_restaurants,

    }
    return render(request, "index.html", context)


def about_view(request):
    context = {

    }

    return render(request, "privacy-policy.html", context)


def list_view(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:

        ip = x_forwarded_for.split(",")[0]

    else:

        ip = request.META.get("REMOTE_ADDR")

    geolocation_json = get_ip_geolocation_data(ip)

    geolocation_data = json.loads(geolocation_json)

    country = geolocation_data["country"]

    region = geolocation_data["region"]

    cont = Countries.objects.filter(name=str(country)).values('slug')

    result = Restaurants.objects.filter(country_of_restaurant__slug__in=cont)

    rating = str(request.GET.get("rating")).split(" ")[0]

    city = request.GET.get("city")

    r_type = request.GET.get("type")

    count = request.GET.get("count")

    if rating:
        try:
            rating = int(rating)
            result = result.filter(rating=rating)
        except ValueError:
            pass
    if city:
        result = result.filter(city__icontains=city)
    if r_type:
        result = result.filter(type_r=r_type)

    if count:
        result = result.filter(available_seats__gte=count)

    if result.count() == 0:
        message = "Ölkəyə yaxud axtarışa uyğun nəticə tapılmadı"
        print(message)
    else:
        message = ""

    paginator = Paginator(result, 6)
    page = request.GET.get('page', 1)
    p = paginator.get_page(page)

    context = {
        'message': message,
        'p': p,
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


def saved_restaurants(request):
    user_restaurants = request.user.wishlist.all()

    paginator = Paginator(user_restaurants, 2)
    page = request.GET.get('page', 1)
    p = paginator.get_page(page)

    if user_restaurants.count() == 0:
        message = "Heç bir restoran əlavə edilməyib"
    else:
        message = ""

    context = {
        'user_restaurants': user_restaurants,
        'p': p,
        'paginator': paginator,
        'message': message,
    }

    return render(request, "wishlist.html", context)


def reserved_view(request):
    context = {

    }

    return render(request, "reserved.html", context)


def star(restaurant, user, rate):
    total_rating = 0
    users = Rating.objects.filter(restaurant=restaurant).values_list("user", flat=True)

    if rate:
        if not (user.id in users):
            if user:
                obj = Rating.objects.create(restaurant=restaurant, user=user, rate=rate)
                obj.save()

    for i in Rating.objects.filter(restaurant=restaurant).values_list("rate", flat=True):
        total_rating += i

    say = Rating.objects.filter(
        restaurant=restaurant
    ).values_list("rate", flat=True).count()

    if say:
        total_rating = total_rating // say

    restaurant.rating = total_rating
    restaurant.save()

    return restaurant.rating


def restaurant_detail_view(request, slug):
    restaurant = get_object_or_404(Restaurants, slug=slug)

    link = "http://localhost:8000/booking/menu/" + slug

    # comment
    form = CommentForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.restaurant = restaurant
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('booking:restaurant_detail', args=[restaurant.slug]))
        else:
            form = CommentForm()
    # comment
    comments = Comment.objects.filter(restaurant=restaurant).order_by("-created_at")
    users = Rating.objects.filter(restaurant=restaurant).values_list("user", flat=True)
    total_rating = star(restaurant, request.user, request.GET.get("rate"))

    context = {
        'restaurant': restaurant,
        'link': link,
        'form': form,
        'total_rating': total_rating,
        'comments': comments,
        'users': users,

    }

    return render(request, "restaurant-detail.html", context)


def menu_restaurant(request, slug):
    restaurant = get_object_or_404(Restaurants, slug=slug)

    context = {
        'restaurant': restaurant,

    }

    return render(request, "menu.html", context)


def reserve_restaurant(request, slug):
    context = {}
    restaurant = get_object_or_404(Restaurants, slug=slug)
    obj = Reserve.objects.filter(user=request.user, restaurant=restaurant)
    obj = list(obj.values_list("user", flat=True))

    if request.method == "POST":

        form = ReserveForm(request.POST or None)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.restaurant = restaurant
            reservation.save()
            form = ReserveForm()

    else:

        form = ReserveForm()

    obyekt = Reserve.objects.filter(user=request.user, restaurant=restaurant)

    if request.method == "POST" and obyekt.first():
        count_guest = obyekt.first().count_of_guest
        if restaurant.available_seats >= count_guest:
            restaurant.available_seats = restaurant.available_seats - count_guest
            restaurant.save()

    context = {
        'restaurant': restaurant,
        'form': form,
        'obj': obj,

    }

    return render(request, "reservation.html", context)


# commentLikeandUnlike
def like_and_unlike(request):
    if request.method == "POST" and request.is_ajax():
        user = request.user
        comment_id = request.POST.get("comment_id")
        comment_obj = get_object_or_404(Comment, id=comment_id)

        # Toggle like
        if user in comment_obj.likers.all():
            comment_obj.likers.remove(user)
        else:
            comment_obj.likers.add(user)

        like, created = Likes.objects.get_or_create(user=user, comment=comment_obj)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

        comment_obj.save()
        like.save()

        data = {
            'value': like.value,
            'likes': comment_obj.likers.all().count()
        }

        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request.'})


def wishlist_create_view(request):
    data = {}

    restaurant_id = request.POST.get("restaurant_id")
    restaurant_obj = get_object_or_404(Restaurants, id=int(restaurant_id))

    if request.user in restaurant_obj.wishlist.all():
        restaurant_obj.wishlist.remove(request.user)
        data['success'] = False
    else:
        restaurant_obj.wishlist.add(request.user)
        data['success'] = True

    return JsonResponse(data)
