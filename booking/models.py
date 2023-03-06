import qrcode
from django.db import models
from services.choices import CHOICES, TIME_CHOICES
from services.uploader import Uploader
from services.mixin import DateMixin, SlugMixin
from services.generator import Generator
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image, ImageDraw
from django.contrib.auth import get_user_model
from io import BytesIO
from django.core.files import File
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


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
    name = models.CharField(max_length=100, )
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


from django.urls import reverse


class Restaurants(DateMixin, SlugMixin):
    name = models.CharField(max_length=200, )
    country_of_restaurant = models.ForeignKey(Countries, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=200, )
    type_r = models.CharField(max_length=100, choices=CHOICES, )
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0, editable=False, null=True, blank=True)
    number = models.TextField()
    location = models.TextField()
    description = models.TextField()
    seats = models.IntegerField(null=True, blank=True, default=1)
    available_seats = models.IntegerField(null=True, blank=True, default=0)
    wishlist = models.ManyToManyField(User, blank=True, related_name="wishlist", editable=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('booking:menu', args=[str(self.slug)])

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

        if not self.images:
            img = Image.open(self.images.path)
            if img.height > 300 or img.width > 300:
                new_img = (626, 600)
                img.thumbnail(new_img)
                img.save(self.images.path)

        super(RestaurantImages, self).save(*args, **kwargs)


class RestaurantMenu(DateMixin, SlugMixin):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    menu_images = models.FileField(upload_to=Uploader.upload_images_for_menu, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=RestaurantMenu)

        if not self.menu_images:
            img = Image.open(self.images.path)
            if img.height > 300 or img.width > 300:
                new_img = (626, 600)
                img.thumbnail(new_img)
                img.save(self.menu_images.path)

        super(RestaurantMenu, self).save(*args, **kwargs)


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


class BlogModel(DateMixin, SlugMixin):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    image = models.ImageField(upload_to=Uploader.upload_images_for_blog)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Blog Model"
        verbose_name_plural = "Blog models"


class Comment(MPTTModel, DateMixin, SlugMixin):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    body = models.TextField(null=True, blank=True)
    likers = models.ManyToManyField(User, default=None, blank=True, related_name='likers')

    def __str__(self):
        return self.user.username

    def user_like_status(self, user):
        if Likes.objects.filter(user=user, comment=self).exists():
            return "Unlike"
        else:
            return "Like"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    @property
    def num_likes(self):
        return self.likers.all().count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=Comment)
        super(Comment, self).save(*args, **kwargs)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


class Likes(DateMixin, SlugMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_likes")
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=Likes)
        super(Likes, self).save(*args, **kwargs)


class Rating(DateMixin, SlugMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, related_name="restaurant")
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

    def __str__(self):
        return f"{self.rate} --> ulduz --> {self.restaurant.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=Rating)
        super(Rating, self).save(*args, **kwargs)


class Reserve(DateMixin, SlugMixin):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    full_name = models.CharField(max_length=100,)
    count_of_guest = models.IntegerField(default=1)
    phone_number = models.TextField()
    passport_number = models.CharField(max_length=100)
    date = models.DateField()
    hour = models.CharField(choices=TIME_CHOICES, max_length=100)
    notes = models.TextField()

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Reserve"
        verbose_name_plural = "Reserves"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=Reserve)
        super(Reserve, self).save(*args, **kwargs)
