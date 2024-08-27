import random
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import UsersAPI, CurrentUserAPI


class TestUrl(TestCase) :
    def test_user_api_url_resolves(self) :
        url = reverse('user_api')
        response = resolve(url)
        self.assertEquals(response.func.view_class, UsersAPI)
    def test_current_user_api_url_resolves(self) :
        url = reverse('current_user_api')
        response = resolve(url)
        self.assertEquals(response.func.view_class, CurrentUserAPI)
    def test_primary_key_user_api_url_resolves(self):
        url = reverse('user_api_with_primary_key',args=[random.randint(0, 1000)])
        response = resolve(url)
        self.assertEquals(response.func.view_class, UsersAPI)
