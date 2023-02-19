from django.db import models
from services.choices import CHOICES
from services.uploader import Uploader
from services.mixin import DateMixin, SlugMixin
from services.generator import Generator
from django.core.validators import MaxValueValidator, MinValueValidator


class Countries(DateMixin, SlugMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Country"
        verbose_name_plural = 'Countries'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=Countries)
        super(Countries, self).save(*args, **kwargs)


class Cities(models.Model):
    name = models.CharField(max_length=100,)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Restaurants(DateMixin, SlugMixin):
    name = models.CharField(max_length=200, )
    country_of_restaurant = models.ForeignKey(Countries, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=200, )
    type_r = models.CharField(max_length=100, choices=CHOICES, )
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    menu = models.FileField(upload_to=Uploader.upload_menu_to_restaurants)
    number = models.TextField()
    location = models.TextField()
    description = models.TextField()
    seats = models.IntegerField(null=True, blank=True, default=1)
    available_seats = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=Restaurants)
        super(Restaurants, self).save(*args, **kwargs)


class RestaurantImages(DateMixin, SlugMixin):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    images = models.FileField(upload_to=Uploader.upload_images_to_restaurants, )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=RestaurantImages)
        super(RestaurantImages, self).save(*args, **kwargs)


class CooperationCompanies(DateMixin, SlugMixin):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=Uploader.upload_images_for_cooperation)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Cooperation-Company"
        verbose_name_plural = "Cooperation-Companies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=CooperationCompanies)
        super(CooperationCompanies, self).save(*args, **kwargs)
