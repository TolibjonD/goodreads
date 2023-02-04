from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from django.contrib.auth import get_user

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

        user = CustomUser.objects.get(username = 'testuser')
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

        user_count = CustomUser.objects.count()
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

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form" , "email" , "Enter a valid email address.")

    def test_username_is_unique(self):
        user = CustomUser.objects.create(
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

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form" , "username", "A user with that username already exists.")

# ============== Login tests beginning =============
class LoginTest(TestCase):
    def test_success_login(self):
        user = CustomUser.objects.create(
            username = 'userjon',
            email = 'userjon@mail.ru'
        )
        user.set_password('userpass')
        user.save()
        self.client.post(
            reverse('users:login'),
            data={
                'username':'userjon',
                'password':'userpass'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_data(self):
        user = CustomUser.objects.create(
            username = 'userjon',
            email = 'userjon@mail.ru'
        )
        user.set_password('userpass')
        user.save()
        self.client.post(
            reverse('users:login'),
            data={
                'username':'wronguser',
                'password':'userpass'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.client.post(
            reverse('users:login'),
            data={
                'username':'userjon',
                'password':'wrong_pass'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
    
    def test_logout(self):
        user = CustomUser.objects.create(
            username = 'testuser',
            first_name = 'testjon',
            last_name = 'testov',
            email = 'test@mail.ru'
        )
        user.set_password("testpass")
        user.save()
        self.client.login(username= 'testuser' , password = 'testpass')
        response = self.client.get(reverse('users:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 302)

class ProfileTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.url, reverse('users:login') + "?next=/users/profile/")
        self.assertEqual(response.status_code, 302)

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username = 'testuser',
            first_name = 'testjon',
            last_name = 'testov',
            email = 'test@mail.ru'
        )
        user.set_password("testpass")
        user.save()
        self.client.login(username= 'testuser' , password = 'testpass')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
    
    def test_update_profile(self):
        user = CustomUser.objects.create(
            username = 'testuser',
            first_name = 'testjon',
            last_name = 'testov',
            email = 'test@mail.ru'
        )
        user.set_password("testpass")
        user.save()
        self.client.login(username= 'testuser' , password = 'testpass')
        response = self.client.post(
            reverse('users:update'),
            data={
                "username":'Jimmy',
                'first_name':'Jim',
                'last_name':'Kerry',
                'email':'Jim@mail.ru'
            }
            )

        user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:profile'))
        self.assertEqual(user.username, 'Jimmy')
        self.assertEqual(user.last_name, 'Kerry')