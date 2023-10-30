from api.models import *
from django.test import TestCase

class NotificationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="demaxl", password="Characters12345!")
        cls.user = User.objects.create_user(username="david", password="Characters12345!")
        cls.article = Article.objects.create(
            author=cls.author,
            title="A test title",
            body="This is a test article")
    
    def testUserLikes(self):
        self.article.like(self.user)

        self.assertIn(self.user, self.article.likes.all())

        self.article.like(self.user)
        self.assertEqual(self.article.likes.count(), 1)

