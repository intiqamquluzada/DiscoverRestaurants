from django.contrib import admin
from .models import (Restaurants, RestaurantImages, CooperationCompanies,
                     Countries, Cities, BlogModel,
                     RestaurantMenu, Comment, Likes)


class ImageInline(admin.StackedInline):
    model = RestaurantImages
    extra = 1
    max_num = 10


class MenuInline(admin.StackedInline):
    model = RestaurantMenu
    extra = 1
    max_num = 10


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [ImageInline, MenuInline]
    list_display = ('name', 'type_r', 'slug', 'country_of_restaurant')
    list_filter = ('created_at', 'rating')


admin.site.register(Restaurants, RestaurantAdmin)
admin.site.register(BlogModel)
admin.site.register(CooperationCompanies)
admin.site.register(Countries)
admin.site.register(Cities)
admin.site.register(Comment)
admin.site.register(Likes)


