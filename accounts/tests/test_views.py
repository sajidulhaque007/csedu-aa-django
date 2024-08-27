from django.test import TestCase, Client
from django.urls import reverse
from accounts.views import *
from rest_framework import status
import json

class TestViews(TestCase) :
    def setUp(self) :
        self.client = Client()
        self.user_api_url = reverse('user_api')
        self.client.post(reverse('branch_api'),{"name":"Sample_Branch","estimated_processing_time":1,"estimated_processing_cost":1})
        self.user_api_post_data = {
            'email': "sampleemail@mail.com",
            'name': "sample_name",
            'password': "sample",
            'role': "office_staff",
            'username': "sample_username",
            'assigned_branch': 1,
        }
        self.user_api_post_invalid_role_data = {
            'email': "sampleemail@mail.com",
            'name': "sample_name",
            'password': "sample",
            'role': "invalid_role",
            'username': "sample_username",
            'assigned_branch': 1,
        }
        self.user_api_post_invalid_branch_data = {
            'email': "sampleemail@mail.com",
            'name': "sample_name",
            'password': "sample",
            'role': "office_data",
            'username': "sample_username",
            'assigned_branch': 2,
        }
        self.user_api_patch_data = {
            'id' : 1,
            'email': "sampleemail@mail.com",
            'name': "sample_name",
            'role': "delivery_man",
            'username': "sample_username",
            'assigned_branch': 1,
        }
        self.user_api_patch_invalid_data = {
            'id' : 1,
            'email': "sampleemail@mail.com",
            'name': "sample_name",
            'role': "delivery_man",
            'username': "sample_username",
            'assigned_branch': 2,
        }
        self.user_api_delete_data = {
            'email': "sampleemail@mail.com",
            'name': "sample_name",
            'password': "sample",
            'role': "office_staff",
            'username': "sample_username",
            'assigned_branch': 1,
            'id':1,
        }
    def test_users_api_get(self) :
        response = self.client.get(self.user_api_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    def test_users_api_post_valid_data(self) :
        response = self.client.post(self.user_api_url, self.user_api_post_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    def test_users_api_post_no_data(self):
        response = self.client.post(self.user_api_url, {})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_users_api_post_invalid_role_data(self):
        response = self.client.post(self.user_api_url, self.user_api_post_invalid_role_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_users_api_post_invalid_branch_data(self):
        response = self.client.post(self.user_api_url, self.user_api_post_invalid_branch_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_users_api_patch_data(self) :
        self.client.post(self.user_api_url, data = json.dumps(self.user_api_post_data), content_type='application/json')
        response = self.client.patch(reverse('user_api_with_primary_key',args=[1]), data = json.dumps(self.user_api_patch_data), content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
    def test_users_api_patch_invalid_data(self) :
        self.client.post(self.user_api_url, data = json.dumps(self.user_api_post_data), content_type='application/json')
        response = self.client.patch(reverse('user_api_with_primary_key',args=[1]), data = json.dumps(self.user_api_patch_invalid_data), content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_users_api_delete_valid_data(self) :
        self.client.post(self.user_api_url, data = json.dumps(self.user_api_post_data), content_type='application/json')
        response = self.client.delete(reverse('user_api_with_primary_key',args=[1]), data = json.dumps(self.user_api_delete_data),content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)