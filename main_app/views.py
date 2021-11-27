from django.shortcuts import render

# from django.http import HttpResponse

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from main_app.models import Post

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class Posts(TemplateView):
    model = Post
    template_name = "posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        # context["query"] = self.kwargs['q']
        return context

class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post"] = Post.objects.filter(id=id)
    #     return context