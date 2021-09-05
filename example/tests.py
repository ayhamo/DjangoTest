from django.test import TestCase
from django.contrib.auth.models import User
from example.models import Post, Category


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
