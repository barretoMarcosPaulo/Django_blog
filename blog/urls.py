from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
]
