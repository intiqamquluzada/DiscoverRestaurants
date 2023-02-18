from django.contrib import admin
from .models import Restaurants, RestaurantImages, CooperationCompanies, Countries, Cities


class ImageInline(admin.StackedInline):
    model = RestaurantImages
    extra = 1
    max_num = 10


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('name', 'type_r', 'slug')
    list_filter = ('created_at', 'rating')


admin.site.register(Restaurants, RestaurantAdmin)

admin.site.register(CooperationCompanies)
admin.site.register(Countries)
admin.site.register(Cities)
