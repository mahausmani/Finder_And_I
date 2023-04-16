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
        self.profile_picture = SimpleUploadedFile("profile_picture.jpg", b"file_content", content_type="image/jpeg")

        self.valid_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
            'profile_picture': self.profile_picture,
        }

    def test_register_view_with_valid_data(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302) #check if it was redirected to another url after the form was posted
        print("Redirecting to:", reverse('login'))
        self.assertRedirects(response, reverse('login'))

        # check user was created
        self.assertTrue(User.objects.filter(username=self.username).exists())

        # check profile was created
        user = User.objects.get(username=self.username)
        self.assertTrue(Profile.objects.filter(user=user).exists())
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.profile_picture, self.valid_data['profile_picture'])

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

# class ProfileViewTestCase(TestCase):
#     # def setUp(self):
#     #     self.client = Client()
#     #     self.url_profile = reverse('profile')
#     #     self.url_login = reverse('login')

#     #     self.user = User.objects.create_user(
#     #         username='testuser', email='testuser@example.com', password='testpassword'
#     #     )
#     #     self.profile = Profile.objects.create(user=self.user)
#     #     self.post_content = 'Test post content'
#     #     self.post_image = SimpleUploadedFile("post_image.jpg", b"file_content", content_type="image/jpeg")
#     #     self.valid_data = {
#     #         'content': self.post_content,
#     #         'image': self.post_image,
#     #     }
#     def setUp(self):
#             self.client = Client()
#             self.url_profile = reverse('/profile/')  
#             print(self.url_profile)
#             self.username = 'test'
#             self.password = 'password'

#             # create a user with the given username and password
#             User.objects.create_user(
#                 username=self.username,
#                 password=self.password
#             )

#     def test_profile_view_with_authenticated_user(self):
#         self.client.login(username=self.username, password=self.password)
#         response = self.client.get(self.url_profile)
#         print(response)
#         # check that the response has status code 200 OK
#         return True
        # self.assertEqual(response.status_code, 200) 
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'users/profile.html')
        # self.assertIsInstance(response.context['form'], CreatePostForm)
        # self.assertIsInstance(response.context['profile'], Profile)
        # self.assertQuerysetEqual(response.context['posts'], [])
        # self.assertContains(response, 'Create Post')
        # self.assertContains(response, 'Log out')


    # def test_profile_view_with_unauthenticated_user(self):
    #     response = self.client.get(self.url_profile)
    #     self.assertRedirects(response, f"{self.url_login}?next={self.url_profile}")

    # def test_profile_view_with_valid_post_data(self):
    #     self.client.login(username='testuser', password='testpassword')
    #     response = self.client.post(self.url_profile, data=self.valid_data)
    #     self.assertRedirects(response, self.url_profile)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(Post.objects.filter(content=self.post_content, author=self.user, image=self.post_image).exists())
    #     self.assertContains(response, 'Your post has been created!')

    # def test_profile_view_with_invalid_post_data(self):
    #     self.client.login(username='testuser', password='testpassword')
    #     invalid_data = self.valid_data.copy()
    #     invalid_data['content'] = '' # set content to empty string to make form invalid
    #     response = self.client.post(self.url_profile, data=invalid_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'users/profile.html')
    #     self.assertContains(response, 'Create Post')
    #     self.assertContains(response, 'This field is required.')
    #     self.assertFalse(Post.objects.filter(author=self.user).exists())
