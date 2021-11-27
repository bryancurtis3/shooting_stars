from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="Home"),
    path('posts/', views.Posts.as_view(), name="posts"),
    path('posts/<int:pk>', views.PostDetail.as_view(), name="post_detail"),
    path('posts/new', views.PostCreate.as_view(), name="post_create"),
    path('posts/<int:pk>/delete', views.PostDelete.as_view(), name="post_delete"),
]
