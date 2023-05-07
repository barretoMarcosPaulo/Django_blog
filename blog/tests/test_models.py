import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from blog.models import Post, Comment


@pytest.mark.django_db
class TestModels:

    @pytest.fixture
    def user(self):
        return User.objects.create(username='testuser')

    @pytest.fixture
    def post(self, user):
        return Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=user,
            content='Test content'
        )

    def test_post_string_representation(self, post):
        assert str(post) == 'Test Post'

    def test_post_get_absolute_url(self, post):
        assert post.get_absolute_url() == '/test-post/'

    def test_post_title_max_length(self, post):
        max_length = post._meta.get_field('title').max_length
        assert max_length == 200

    def test_post_slug_max_length(self, post):
        max_length = post._meta.get_field('slug').max_length
        assert max_length == 200

    def test_post_created_on_auto_now_add(self, post):
        assert post.created_on is not None

    def test_post_updated_on_auto_now(self, post):
        old_updated_on = post.updated_on
        post.content = 'Updated test content'
        post.save()
        assert post.updated_on > old_updated_on


    def test_create_comment(self, post):
        comment = Comment.objects.create(
            post=post,
            name="Joao",
            email="Joao@test.com",
            body="Muito bom"
        )
        assert str(comment) == "Comentário Muito bom por Joao"


    def test_comment_active(self, post):
        comment = Comment.objects.create(
            post=post,
            name="Joao",
            email="Joao@test.com",
            body="Teste de comentário"
        )
        assert comment.active == False
        comment.active = True
        comment.save()
        assert comment.active == True

    def test_comment_ordering(self, post):
        comment1 = Comment.objects.create(
            post=post,
            name="Joao",
            email="Joao@test.com",
            body="Comentário do joao"
        )
        comment2 = Comment.objects.create(
            post=post,
            name="ana",
            email="ana@test.com",
            body="comentário da ana"
        )
        comments = Comment.objects.all()
        assert comments[0] == comment1
        assert comments[1] == comment2