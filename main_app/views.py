from django.db.models import fields
from django.shortcuts import render

from django.urls import reverse

# from django.http import HttpResponse

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.forms import ModelForm, TextInput


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
        form = PostCreateForm()
        context["form"] = form
        return context

class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"

class PostCreate(CreateView):
    model = Post
    fields = ['title', 'image', 'description', 'lat', 'long']
    template_name = "post_create.html"
    success_url = "/posts/"

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreate, self).form_valid(form)

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'description', 'lat', 'long']
        widgets = {
            'title': TextInput(attrs={'class': 'myfieldclass'}),
        }

