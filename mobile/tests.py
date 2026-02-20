from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class MobileHomeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_home_view_redirects_to_login(self):
        """If not logged in, should redirect to login page."""
        response = self.client.get(reverse('mobile:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_home_view_accessible_when_logged_in(self):
        """If logged in, should return 200 OK and use correct template."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('mobile:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mobile/home.html')
        self.assertTemplateUsed(response, 'mobile/css_and_javascript.html')
        self.assertContains(response, 'Mobile Play Queue')
