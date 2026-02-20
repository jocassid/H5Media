from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LoginRedirectionTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')

    def test_login_desktop_redirects_to_home(self):
        """Selecting desktop mode (or default) should redirect to main home."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
            'mode': 'desktop'
        })
        # Default LOGIN_REDIRECT_URL is '/' (home)
        self.assertRedirects(response, reverse('home'))

    def test_login_mobile_redirects_to_mobile_home(self):
        """Selecting mobile mode should redirect to mobile home."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
            'mode': 'mobile'
        })
        self.assertRedirects(response, reverse('mobile:home'))

    def test_login_no_mode_redirects_to_home(self):
        """If no mode is provided, should use default redirection."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('home'))
