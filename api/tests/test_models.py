from api.models import *
from django.test import TestCase

class ModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="demaxl", password="Characters12345!")
        cls.user = User.objects.create_user(username="david", password="Characters12345!")
        cls.article = Article.objects.create(
            author=cls.author,
            title="A test title",
            body="This is a test article")
        
        cls.comment = Comment.objects.create(
            article=cls.article,
            user=cls.user,
            body="A test comment"
        )

        cls.reply = Reply.objects.create(
            comment=cls.comment,
            user=cls.author,
            body="A test reply"
        )
    
    def testUserLikes(self):
        self.article.like(self.user)

        self.assertIn(self.user, self.article.likes.all())

        self.article.like(self.user)
        self.assertEqual(self.article.likes.count(), 1)

    def testCommentLike(self):
        self.comment.like(self.user)
        
        self.assertIn(self.user, self.comment.likes.all())

        self.reply.like(self.user)
        self.assertIn(self.user, self.reply.likes.all())

    def testCreateProfile(self):
        user = User.objects.create_user(username="test", password="Characters12345!")
        user.save()

        self.assertEqual(Profile.objects.get(user=user).user, user)





