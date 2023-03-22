# it is good approach to separate all business logic into the so called services
# instead of spreading across views. Try to stick "Layered Architecture" approach,
# as an example you can see here https://github.com/edodo1337/django-react/tree/master/backend/billing/logic

class Uploader:

    @staticmethod
    def upload_menu_to_restaurants(instance, filename):
        return f"restaurants/{instance.slug}/{filename}"

    @staticmethod
    def upload_images_to_restaurants(instance, filename):
        return f"restaurantsImage/{instance.slug}/{filename}"

    @staticmethod
    def upload_images_for_cooperation(instance, filename):
        return f"companies/{instance.slug}/{filename}"

    @staticmethod
    def upload_images_for_blog(instance, filename):
        return f"blog/{instance.slug}/{filename}"

    @staticmethod
    def upload_images_for_menu(instance, filename):
        return f"menu/{instance.slug}/{filename}"

    @staticmethod
    def upload_images_for_user(instance, filename):
        return f"user/{instance.slug}/{filename}"



