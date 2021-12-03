from django.db.models import fields
from django.forms.widgets import Input
from django.shortcuts import render, redirect

from django.urls import reverse

from django.db.models import Q

# from django.http import HttpResponse

# Views imports
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Authentication imports
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# from django.http import request
from django.contrib import messages
from django.forms import ModelForm, TextInput, Form, CharField, ValidationError, PasswordInput


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
        context["login_form"] = LoginForm()
        context["location_form"] = UserUpdateForm()

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
        context["login_form"] = LoginForm()
        context["location_form"] = UserUpdateForm()


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

        # Auth forms
        context = super().get_context_data(**kwargs)
        context["signup_form"] = CustomUserCreationForm()
        context["login_form"] = AuthenticationForm()
        context["location_form"] = UserUpdateForm()


        # Get, sanitize, and prepare user query
        query = self.request.GET.get("q")
        userPosts = self.request.GET.get("user")

        if query:
            query = query.replace(" ", "")
            latitude = query.split(",")[0]
            longitude = query.split(",")[1]

            # Code for loose searching coord similarity
            latOne = float(latitude)
            latTwo = float(latitude)

            longOne = float(longitude)
            longTwo = float(longitude)

            if latOne < 0:
                latOne += .1
                latTwo -= .1
            else:
                latOne -= .1
                latTwo += .1

            if longOne < 0:
                longOne += .1
                longTwo -= .1
            else:
                longOne -= .1
                longTwo += .1

            context["posts"] = Post.objects.filter(
                Q(lat__gte = latOne) & Q(lat__lte = latTwo) &
                Q(long__gte = longOne) & Q(long__lte = longTwo)
            ).order_by('created_at')
        else:
            context["posts"] = Post.objects.all().order_by('created_at')

        if userPosts:
            context["posts"] = Post.objects.filter(user_id = userPosts)

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

        # Auth forms
        context = super().get_context_data(**kwargs)
        context["signup_form"] = CustomUserCreationForm()
        context["login_form"] = AuthenticationForm()
        context["location_form"] = UserUpdateForm()


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
            return redirect("post_detail", pk=pk)
        else:
            # idk about this
            context = {"form": form, "pk": pk}
            return render(request, "posts/posts.html", context)


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


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['location']

class UserUpdate(View):
    def post(self, request, pk):

        form = UserUpdateForm(request.POST)
        if form.is_valid():
            User.objects.filter(pk=pk).update(location=request.POST.get('location'))
            return redirect("home")
        else:
            messages.warning(self.request, 'Form submission error, plese try again.')
            context = {'login_form': LoginForm(), "signup_form": UserCreationForm(), 'location_form': form}
            return render(request, "home.html", context)


# === Auth Views ===
class Signup(View):

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else: 
            messages.warning(self.request, 'Form submission error, plese try again.')
            context = {'login_form': LoginForm(), "signup_form": form}
            return render(request, "home.html", context)


class LoginForm(Form):
    username = CharField(max_length=255, required=True)
    password = CharField(widget=PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class Login(View):

    def post(self, request):
        form = LoginForm(request.POST or None)
         
        if request.POST and form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect("/")

        # maybe try to reshow modals with contexts
        messages.warning(self.request, 'Form submission error, plese try again.')
        return render(request, 'home.html', {'login_form': form, 'signup_form': CustomUserCreationForm(), 'loginError': 'error'})


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