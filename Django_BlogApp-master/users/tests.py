from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile,Post
from users.forms import UserRegisterForm, CreatePostForm

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'

        self.valid_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        }

    def test_register_view_with_valid_data(self):
        response = self.client.post(self.url, data=self.valid_data)
        
        user_exists = User.objects.filter(username=self.username).exists()
        self.assertTrue(user_exists, msg="User should have been created")

        # check profile was created
        user = User.objects.get(username=self.username)
        profile_exists = Profile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists, msg="Profile should have been created")

        self.assertEqual(response.status_code, 302) #check if it was redirected to another url after the form was posted
        print("Redirecting to:", reverse('login'))
        self.assertRedirects(response, reverse('login'))

    def test_register_view_with_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['username'] = ''  # set username to empty string to make form invalid
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertFalse(User.objects.filter(username=self.username).exists())
        self.assertFalse(Profile.objects.filter(user__username=self.username).exists())

    def test_register_view_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserRegisterForm)
        self.assertTemplateUsed(response, 'users/register.html')



class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('profile')
        self.url_login = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        image_file = SimpleUploadedFile('test_image.jpg',  b"file_content", content_type="image/jpeg")
        self.profile = Profile.objects.create(user=self.user, profile_picture=image_file)

    def test_profile_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, self.user.username)

    def test_profile_view_with_unauthenticated_user(self):
            response = self.client.get(self.profile_url)
            self.assertRedirects(response, f"{self.url_login}?next={self.profile_url}")

    def test_create_post_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('profile'), {'content': 'Test post content'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.content, 'Test post content')
        self.assertEqual(post.author, self.user)

    def test_create_post_with_unauthenticated_user(self):
        response = self.client.post(reverse('profile'), {'content': 'Test post content'})
        self.assertRedirects(response, f"{self.url_login}?next={self.profile_url}")
        self.assertEqual(Post.objects.count(), 0)

    
