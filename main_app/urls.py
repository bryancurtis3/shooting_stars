from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="Home"),
    path('posts/', views.Posts.as_view(), name="posts"),
    path('posts/<int:pk>', views.PostDetail.as_view(), name="post_detail"),
]
