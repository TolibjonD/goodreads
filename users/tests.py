from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# ========= The test of Registration beginning =========
class RegisterTest(TestCase):
    def test_user_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username':'testuser',
                'first_name':'testjon',
                'last_name':'testbekov',
                'email':'test@mail.ru',
                'password':'testpass'
            }
        )

        user = User.objects.get(username = 'testuser')
        self.assertEqual(user.first_name, "testjon")
        self.assertEqual(user.last_name, "testbekov")
        self.assertEqual(user.email, "test@mail.ru")
        self.assertNotEqual(user.password, "testpass")
        self.assertTrue(user.check_password('testpass'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name':'testjon',
                'last_name':'testbekov',
                'email':'test@mail.ru',
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form" , "username" , "This field is required.")
        self.assertFormError(response, "form" , "password" , "This field is required.")

    def test_email_field(self):
        response = self.client.post(
            reverse('users:register'),
          data={
                'username':'testuser',
                'first_name':'testjon',
                'last_name':'testbekov',
                'email':'wrong-email',
                'password':'testpass'
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form" , "email" , "Enter a valid email address.")

    def test_username_is_unique(self):
        user = User.objects.create(
            username = 'testuser',
            first_name = 'testjon',
            last_name = 'testov',
            email = 'test@mail.ru'
        )
        user.set_password("testpass")
        user.save()
        response = self.client.post(
            reverse('users:register'),
            data={
                'username':'testuser',
                'first_name':'testjon',
                'last_name':'testbekov',
                'email':'test@mail.ru',
                'password':'testpass'
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form" , "username", "A user with that username already exists.")