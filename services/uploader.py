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



