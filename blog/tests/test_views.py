import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from mixer.backend.django import mixer

from django.contrib.auth.models import User

from blog.views import PostList
from blog.models import Post


@pytest.mark.django_db
class TestPostList:

    @pytest.fixture
    def user(self):
        return User.objects.create(username='testuser')

    def test_post_list_view(self, client):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200
        assert isinstance(response.context_data['view'], PostList)
        assert 'object_list' in response.context_data
        assert len(response.context_data['object_list']) == Post.objects.filter(status=1).count()

    def test_post_list_view_status_code(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_post_list_view_uses_correct_template(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'index.html')

    def test_post_list_view_paginated_by_three(self, client, user):
        Post.objects.bulk_create([
            Post(title=f"Post {i}", slug=f"post-{i}", author=user, content="test", status=1)
            for i in range(10)
        ])
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert len(response.context['object_list']) == 3

    def test_post_list_status_draft(self, client, user):
        Post.objects.bulk_create([
            Post(title=f"Post {i}", slug=f"post-{i}", author=user, content="test", status=0)
            for i in range(10)
        ])
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert len(response.context['object_list']) == 0

    def test_post_list_view_only_published_posts(self, client, user):
        Post.objects.create(title="Draft Post", slug="draft-post", author=user, content="test", status=0)
        published_post = Post.objects.create(title="Published Post", slug="published-post", author=user, content="test", status=1)
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert published_post in response.context['object_list']
        assert len(response.context['object_list']) == 1

    def test_post_list_view_posts_ordered_by_created_on_descending(self, client, user):
        Post.objects.bulk_create([
            Post(title=f"Post {i}", slug=f"post-{i}", author=user, content="test")
            for i in range(5)
        ])
        response = client.get(reverse('home'))
        assert response.status_code == 200
        posts = response.context['object_list']
        for i in range(1, len(posts)):
            assert posts[i].created_on >= posts[i-1].created_on




@pytest.mark.django_db
class TestPostDetailView:

    def test_get(self, client):
        post = mixer.blend('blog.Post')
        comment = mixer.blend('blog.Comment', post=post, active=True)
        response = client.get(reverse('post_detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200
        assert response.context["comments"][0] == comment
        assert response.context["post"] == post

    def test_get_invalid_slug(self, client):
        response = client.get(reverse('post_detail', kwargs={'slug': 'invalid-slug'}))
        assert response.status_code == 404

    def test_get_no_comments(self, client):
        post = mixer.blend('blog.Post')
        response = client.get(reverse('post_detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200
        assert response.context["comments"].count() == 0

    def test_post_valid_form(self, client):
        post = mixer.blend('blog.Post')
        comment = mixer.blend('blog.Comment', post=post, active=True)
        form_data = {'name': 'Joao', 'email': 'joao@teste.com', 'body': 'Isso é um comentário.'}
        response = client.post(reverse('post_detail', kwargs={'slug': post.slug}), data=form_data)
        assert response.status_code == 200

    def test_post_invalid_form(self, client):
        post = mixer.blend('blog.Post')
        comment = mixer.blend('blog.Comment', post=post, active=True)
        form_data = {'name': '', 'email': '', 'body': ''}
        response = client.post(reverse('post_detail', kwargs={'slug': post.slug}), data=form_data)
        assert response.status_code == 200
        assert response.context["comment_form"].errors
        assert response.context["comments"][0] == comment

    def test_post_no_form_data(self, client):
        post = mixer.blend('blog.Post')
        comment = mixer.blend('blog.Comment', post=post, active=True)
        response = client.post(reverse('post_detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200
        assert response.context["comment_form"].errors
        assert response.context["comments"][0] == comment



