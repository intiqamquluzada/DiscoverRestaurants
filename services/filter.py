
class RestaurantFilter:

    def __init__(self, request, restaurants, query_params):
        self.request = request
        self.restaurants = restaurants
        self.query_params =query_params

    @staticmethod
    def filter_by_country(request, restaurants, query_params):
        if "q" in request.GET:
            country = request.GET.get("q")
            if country:
                query_params += f"country={country}"
                restaurants = restaurants.filter(
                    country_of_restaurant__name__icontains=country
                )
        return restaurants, query_params

    def filter_all(self):
        restaurants, query_params =self.filter_by_country(self.request, self.restaurants, self.query_params)

