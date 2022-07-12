from rest_framework.test import APITestCase

from .models import Place, Restaurant, User, Referral, Item, Category, SubCategory


class RestaurantTestCase(APITestCase):
    def test_restaurant_creation(self):
        initial_restaurants_count = Restaurant.objects.count()
        restaurant_attrs = {'name': 'МакДональдз. Тестовий', 'longitude': 12.4, 'latitude': 56.7}
        response = self.client.post('/api/restaurants/', restaurant_attrs)
        # TODO: need an authenticated user to create a restaurant
        if response.status_code == 201:
            print(response.data)
        self.assertEqual(Restaurant.objects.count(), initial_restaurants_count + 1)
        for attr, expected_value in restaurant_attrs.items():
            self.assertEqual(response.data[attr], expected_value)

    def test_restaurant_deletion(self):
        initial_restaurants_count = Restaurant.objects.count()
        restaurant_id = Restaurant.objects.first().id
        self.client.delete(f'/api/restaurants/{restaurant_id}/')
        # TODO: need an authenticated user to create a restaurant
        self.assertEqual(Restaurant.objects.count(), initial_restaurants_count - 1)
        self.assertRaises(Restaurant.DoesNotExist, Restaurant.objects.get, id=restaurant_id)

    def test_restaurant_list(self):
        initial_restaurants_count = Restaurant.objects.count()
        response = self.client.get('/api/restaurants/')
        self.assertEqual(len(response.data), initial_restaurants_count)

    def test_restaurant_updating(self):
        restaurant = Restaurant.objects.first()
        response = self.client.patch(f'/api/restaurants/{restaurant.id}/', {'name': 'МакДональдз. Тестовий'},
                                     format='json')
        updated = Restaurant.objects.get(id=restaurant.id)
        self.assertEqual(updated.name, 'МакДональдз. Тестовий')
