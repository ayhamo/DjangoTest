from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from example.models import Post, Category
from django.contrib.auth.models import User
from django.test import TestCase


class Test_Create_Post(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_c = Category.objects.create(name='djnago')
        test_u1 = User.objects.create_user(username='test_user1', password='123456789')
        test_p = Post.objects.create(category_id=1, title='Post Title', excerpt='gg',
                                     content='gg', slug='post-title', author_id=1, status='published')

    def test_example_content(self):
        post = Post.postobjects.get(id=1)
        cate = Category.objects.get(id=1)
        author = f'{post.author}'
        self.assertEqual(author, 'test_user1')


class PostTest(APITestCase):
    def test_view_posts(self):
        url = reverse('blog_api:listcreate')
        response = self.client.generic(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_post(self):
        self.test_c = Category.objects.create(name='djnano')

        self.testuser1 = User.objects.create_user(username='test_user1', password='123456789')

        data = {"title": 'new', "author": 1,
                "excerpt": "new", "content": "new"}
        url = reverse('example_api:listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
