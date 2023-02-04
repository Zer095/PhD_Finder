from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import CustomUser, Profile
from positions.models import Position
from positions.tests import create_position
# Create your tests here.

# Test Custom User Position


class CustomUserTest(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create(username = 'TestUser0', email = 'test@user.com', password = '12345')
        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.username, 'TestUser0')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff) 

class ProfileTest(TestCase):

    def test_create_profile(self):
        user = CustomUser.objects.create(username = 'TestUser1', email = 'test@user.com', password = '12345')
        # Check the existance of the profile
        self.assertEqual(Profile.objects.get(user_id = user.id), user.profile)
        self.assertEqual(user.profile.saved, [])

    def test_saved(self):
        user = CustomUser.objects.create(username = 'TestUser2', email = 'test@user.com', password = '12345')
        # Check that profile.save stores position.id
        position = create_position(pos_title='TestPosition', days=0, delta=1)
        user.profile.saved.append(position.id)
        user.profile.save()
        self.assertQuerysetEqual(Position.objects.get(id=user.profile.saved[0]).pos_title, 'TestPosition')


# Test Views
class TestProfileView(TestCase):

    def test_no_user(self):
        response = self.client.get(reverse('users:users-profile'))
        self.assertEqual(response.status_code, 302)

    def test_user_logged(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        c = Client()
        login = self.client.login(username='testuser', password='testpassword')
        # print(login)
        self.assertTrue(login)

        response = self.client.get(reverse('users:users-profile'))
        # Check that the saved position_array is empty
        self.assertEqual(response.context['saved'], [])