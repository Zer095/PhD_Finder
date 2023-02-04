import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from .models import Position
from users.models import CustomUser
# Create your tests here.

class PositionModelTest(TestCase):

    # Test for the method was_published_recently()
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for position whose pos_pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_position = Position(pos_pub_date=time)
        self.assertIs(future_position.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for positions whose pub_date
        is older than 5 days.
        """

        time = timezone.now() - datetime.timedelta(days=5, seconds=1)
        old_positions= Position(pos_pub_date = time)
        self.assertIs(old_positions.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for Questions whos pub_date is 
        within the last five days
        """

        time = timezone.now() - datetime.timedelta(days=4, hours=23, minutes=59, seconds=59)
        recent_position = Position(pos_pub_date = time)
        self.assertIs(recent_position.was_published_recently(), True)


    # Test for the method is_expired()
    def test_is_expired_with_future_expiring_date(self):
        """
        is_expired() returns False for positions whose pos_exp_date is in the future
        """

        time = timezone.now() + datetime.timedelta(days=+5)
        future_position = Position(pos_exp_date=time)
        self.assertIs(future_position.is_expired(), False)

    def test_is_expired_with_past_expiring_date(self):
        """
        is_expired() returns True for positions whose pos_exp_date is in the past
        """

        time = timezone.now() + datetime.timedelta(days=-4)
        past_position = Position(pos_exp_date=time)
        self.assertIs(past_position.is_expired(), True)


# Fuction to create a position
def create_position(pos_title, days, delta):
    """
    Create a position with the given 'pos_title' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published) and
    expires a number of 'delta' offset to pub_date
    """

    time_pub = timezone.now() + datetime.timedelta(days=days)
    time_exp = time_pub + datetime.timedelta(days=delta)

    return Position.objects.create(pos_title=pos_title, pos_pub_date = time_pub, pos_exp_date = time_exp)

# Test for view, PositionDetailView
class PositionDetailViewTests(TestCase):

    def test_no_positions(self):
        """
        if no position exists, an appropriate message is displayed.
        """

        response = self.client.get(reverse('positions:detail', kwargs={'region':'Europe'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No positions are available.")
        self.assertQuerysetEqual(response.context['positions_in_region'], [])

    def future_position(self):
        """
        Positions with a pos_pub_date in the future aren't shown. 
        """
        create_position(pos_title="Future position", days=30, delta=35)
        response = self.client.get(reverse('positions:detail', kwargs={'region':'Europe'}))
        self.assertContains(response, 'No positions are available.')
        self.assertQuerysetEqual(response.context['positions_in_region'], [])

    def expired_position(self):
        """
        Positions with a pos_exp_date in the past arent' shown.
        """
        create_position(pos_title="Expired position", days=-5, delta=-4)
        response = self.client.get(reverse('positions:detail', kwargs={'region':'Europe'}))
        self.assertContains(response, 'No positions are available.')
        self.assertQuerysetEqual(response.context['positions_in_region'], [])

# Test for view, PositionsDescriptionView
class PositionsDescriptionViewTest(TestCase):

    def test_position_does_not_exist(self):
        """
        if the position does not exist, returns a 404 not found
        """

        response = self.client.get(reverse('positions:description', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)
        


class PositionsRegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('positions:register')

    def test_register_view(self):
        response = self.client.get((self.register_url))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'positions/register.html')

        # Test with valid data
        data = {
            'username': 'TestUser',
            'email': 'test@example.com',
            'password1': '-Halleyciccia23',
            'password2': '-Halleyciccia23',
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/positions/')
        self.assertEqual(response.wsgi_request.user.username, 'TestUser')

        # Test with invalid data
        data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('positions:login')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'positions/login.html')

        # Test with valid data
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/positions/')
        self.assertEqual(response.wsgi_request.user.username, 'testuser')

        # Test with invalid data
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'positions/login.html')
