from django.shortcuts import render, redirect
from django.db.models import F
from .models import Restaurants, CooperationCompanies, Countries, Comment, Likes
import requests
import json
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm

api_key = "5117dbe9476548a6834433afd9b63554"

api_url = "https://ipgeolocation.abstractapi.com/v1/?api_key=" + api_key


def get_ip_geolocation_data(ip_address):
    # not using the incoming IP address for testing

    print(ip_address)

    response = requests.get(api_url)

    return response.content


User = get_user_model()


def home_view(request):
    companies_corporation = CooperationCompanies.objects.all()
    rate = Restaurants.objects.all().values_list('rating', flat=True)
    print(rate)
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
    print(country)
    region = geolocation_data["region"]
    print(region)
    # cont = Countries.objects.filter(name=str(country)).values('slug')

    # print(cont)

    result = Restaurants.objects.all()

    search = request.GET.get('q', None)

    print(search)

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

    print(rating)

    city = request.GET.get("city")

    print(city)

    r_type = request.GET.get("type")

    print(r_type)

    count = request.GET.get("count")

    print(count)

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


def save_restaurants(request):
    context = {

    }

    return render(request, "wishlist.html", context)


def reserved_view(request):
    context = {

    }

    return render(request, "reserved.html", context)


from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse


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
    # # comment
    comments = Comment.objects.filter(restaurant=restaurant).order_by("-created_at")

    context = {
        'restaurant': restaurant,
        'link': link,
        'form': form,

        'comments': comments,

    }

    return render(request, "restaurant-detail.html", context)


def menu_restaurant(request, slug):
    restaurant = get_object_or_404(Restaurants, slug=slug)

    context = {
        'restaurant': restaurant,

    }

    return render(request, "menu.html", context)


def reserve_restaurant(request, slug):
    restaurant = get_object_or_404(Restaurants, slug=slug)
    context = {
        'restaurant': restaurant,
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


def wishlist_remove_view(request):
    data = {}

    restaurant_id = request.POST.get("restaurant_id")
    restaurant_obj = get_object_or_404(Restaurants, id=int(restaurant_id))

    if request.user in restaurant_obj.wishlist.all():
        data['success'] = False
        restaurant_obj.wishlist.remove(request.user)

    else:
        data['success'] = False
        restaurant_obj.wishlist.add(request.user)
    return JsonResponse(data)
