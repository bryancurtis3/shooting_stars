from django.db.models import fields
from django.forms.widgets import Input
from django.shortcuts import render, redirect

from django.urls import reverse

# from django.http import HttpResponse

# Views imports
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Authentication imports
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# from django.http import request
from django.contrib import messages
from django.forms import ModelForm, TextInput


from main_app.models import Post, User

# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "location"]

class IncludeAuthForms:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signup_form"] = CustomUserCreationForm()
        context["login_form"] = AuthenticationForm()
        return context

# class CustomUserCreationForm(UserCreationForm):

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = UserCreationForm.Meta.fields + ('custom_field',)


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signup_form"] = CustomUserCreationForm()
        context["login_form"] = AuthenticationForm()

        # Home route shouldn't need this?? ===
        # Get, sanitize, and prepare user query
        # query = self.request.GET.get("q")
        # if query:
        #     latitude = query.split(",")[0]
        #     longitude = query.split(" ")[1]
        #     context["posts"] = Post.objects.filter(
        #         lat__istartswith = latitude,
        #         long__istartswith = longitude
        #     )
        # else:
        #     context["posts"] = Post.objects.all()
        
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
            ).order_by('created_at')
        else:
            context["posts"] = Post.objects.all().order_by('created_at')
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

@method_decorator(login_required, name='dispatch')
class PostCreate(View):

    # Modeled after PostUpdate exploria
    def post(self, request):
        title = request.POST.get('title')
        image = request.POST.get('image')
        description = request.POST.get('description')
        lat = request.POST.get('lat')
        long = request.POST.get('long')

        image_time = request.POST.get('image_time')
        created_at = request.POST.get('created_at')
        updated_at = request.POST.get('updated_at')

        new_post = Post.objects.create(title=title, image=image, description=description, lat=lat, long=long, image_time=image_time, created_at=created_at, updated_at=updated_at, user=request.user)
        return redirect("post_detail", pk=new_post.pk)
        
@method_decorator(login_required, name='dispatch')
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
            pass


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'description', 'lat', 'long', 'image_time']
        widgets = {
            'title': TextInput(attrs={'class': 'myfieldclass'}),
            'image_time': TextInput(attrs={'type': 'date'}),
            
        }
    
    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['image_time'].required = False

@method_decorator(login_required, name='dispatch')
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



class Signup(View):

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else: 
            messages.warning(self.request, 'Form submission error, plese try again.')
            context = {"form": form}
            return redirect("/")


    # def post(self, request):
    #     title = request.POST.get("title")
    #     image = request.POST.get("image")
    #     description = request.POST.get('description')
    #     lat = request.POST.get('lat')
    #     long = request.POST.get('long')

    #     new_post = Post.objects.create(title=title, image=image, description=description, lat=lat, long=long, user=request.user)
    #     return redirect("post_detail", pk=new_post.pk)



# Auth
# class Signup(TemplateView):
#     template_name = "signup.html"

#     def get(self, request):
#         form = UserCreationForm()
#         context = {"form": form}
#         return render(request, "registration/signup.html", context)
    
#     def post(self, request):
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("home")
#         else:
#             # write dtl to accept this message and auto display modal with warning inside after going back to submission page
#             messages.warning(self.request, 'Form submission error, plese try again.')
#             context = {"form": form}
#             return redirect("back")
#             return render(request, "registration/signup.html", context) # FIXME - if invalid form input, how to redirect back to modal form? Currently redirecting to unused signup page