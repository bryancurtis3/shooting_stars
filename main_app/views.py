from django.db.models import fields
from django.shortcuts import render, redirect

from django.urls import reverse

# from django.http import HttpResponse

# Views imports
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Authentication imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# from django.http import request
from django.contrib import messages
from django.forms import ModelForm, TextInput


from main_app.models import Post

# Create your views here.

class IncludeAuthForms:
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["signup_form"] = UserCreationForm()
    context["login_form"] = AuthenticationForm()
    return context



class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signup_form"] = UserCreationForm()
        context["login_form"] = AuthenticationForm()

        # Get, sanitize, and prepare user query
        query = self.request.GET.get("q")
        if query:
            latitude = query.split(",")[0]
            longitude = query.split(" ")[1]
            context["posts"] = Post.objects.filter(
                lat__istartswith = latitude,
                long__istartswith = longitude
            )
        else:
            context["posts"] = Post.objects.all()
        
        return context

# === Post routes ===
class Posts(TemplateView):
    model = Post
    template_name = "posts/posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get, sanitize, and prepare user query
        query = self.request.GET.get("q")
        if query:
            latitude = query.split(",")[0]
            longitude = query.split(" ")[1]
            context["posts"] = Post.objects.filter(
                lat__istartswith = latitude,
                long__istartswith = longitude
            )
        else:
            context["posts"] = Post.objects.all()
        form = PostCreateForm()
        context["form"] = form
        return context

class PostDetail(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostUpdateForm, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostUpdateForm(instance=Post.objects.get(pk=self.kwargs.get("pk")))
        context["form"] = form
        return context

class PostCreate(View):
            

    # Modeled after PostUpdate exploria
    def post(self, request):
        title = request.POST.get("title")
        image = request.POST.get("image")
        description = request.POST.get('description')
        lat = request.POST.get('lat')
        long = request.POST.get('long')

        new_post = Post.objects.create(title=title, image=image, description=description, lat=lat, long=long, user=request.user)
        return redirect("post_detail", pk=new_post.pk)
        

# class PostCreate(CreateView):
#     model = Post
#     fields = ['title', 'image', 'description', 'lat', 'long']
#     template_name = "post_create.html"
#     success_url = "/posts/"

#     def get_success_url(self):
#         return reverse('post_detail', kwargs={'pk': self.object.pk})

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(PostCreate, self).form_valid(form)

class PostUpdate(View):

    def post(self, request, pk):

        form = PostUpdateForm(request.POST)
        if form.is_valid():
            Post.objects.filter(pk=pk).update(title=request.POST.get('title'), image=request.POST.get('image'), description=request.POST.get('description'), lat=request.POST.get('lat'), long=request.POST.get('long'))
            return redirect("posts")
        else:
            # idk about this
            context = {"form": form, "pk": pk}
            return render(request, "posts/posts.html", context)

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'description', 'lat', 'long']
        widgets = {
            'title': TextInput(attrs={'class': 'myfieldclass'}),
        }

class PostDelete(DeleteView):
    model = Post
    success_url = "/posts/"

    def get_success_url(self):
        messages.success(self.request, 'Post successfully deleted.')
        return reverse('posts')

class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'description', 'lat', 'long']
# === End Post Routes ===
    



# Auth
class Signup(TemplateView):
    template_name = "signup.html"

    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            # write dtl to accept this message and auto display modal with warning inside after going back to submission page
            messages.warning(self.request, 'Form submission error, plese try again.')
            context = {"form": form}
            return redirect("back")
            return render(request, "registration/signup.html", context) # FIXME - if invalid form input, how to redirect back to modal form? Currently redirecting to unused signup page