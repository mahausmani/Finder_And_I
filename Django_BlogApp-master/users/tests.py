from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile,Post, FriendRequest
from users.forms import UserRegisterForm, CreatePostForm



class FriendRequestTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')

        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)
        self.profile3 = Profile.objects.get(user=self.user3)

    
    def test_send_friend_request(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('send_friend_request', args=['user2']))
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())
    
    def test_send_friend_request_already_friends(self):
        self.profile1.friends.add(self.user2)
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('send_friend_request', args=['user2']))
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())
    
    def test_send_friend_request_already_sent(self):
        FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('send_friend_request', args=['user2']))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())
    
    def test_accept_friend_request(self):
        friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('accept_friend_request', args=[friend_request.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.profile2.friends.filter(username='user1').exists())
        self.assertTrue(self.profile1.friends.filter(username='user2').exists())
        self.assertFalse(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())
    
    def test_reject_friend_request(self):
        friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('reject_friend_request', args=[friend_request.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())
    
class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)

    def test_user_profile_non_friends_not_displayed(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('your_friends'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'user2')  # Check if the non-friend's username is not displayed

    def test_user_profile_friends_displayed(self):
        self.profile1.friends.add(self.user2)

        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('your_friends'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user2')  # Check if the friend's username is displayed


class FriendRequestTestCaseDisplay(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)
        self.request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)

    def test_display_friend_requests(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user2')  # Check if the sender's username is displayed

    def test_accept_friend_request(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('accept_friend_request', args=[self.request.id]))

        self.assertEqual(response.status_code, 302)
        self.profile2.refresh_from_db()
        self.assertIn(self.user1, self.profile2.friends.all())  # Check if the sender is added to the friend list

    def test_accepted_friend_request_updates_sender(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('accept_friend_request', args=[self.request.id]))

        self.assertEqual(response.status_code, 302)
        self.profile1.refresh_from_db()
        self.assertIn(self.user2, self.profile1.friends.all())  # Check if the receiver is added to the friend list

    def test_decline_friend_request(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('reject_friend_request', args=[self.request.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(FriendRequest.objects.filter(id=self.request.id).exists())  # Check if the request is deleted
