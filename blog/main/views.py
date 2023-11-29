from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect 

from .models import *
from .forms import *
from .utils import *

from django.views.generic import ListView, DetailView, CreateView, View, RedirectView
from django.contrib.auth.views import LoginView

# Create your views here.

class HomeView(DataMixin, ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title='Главная страница')
        return context | base_context
    
    def get_queryset(self):
        return Post.objects.all()
    
class AboutView(DataMixin, View):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        base_context = self.get_user_context(title='О нас')
        return base_context
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    
class LoginUserView(DataMixin, LoginView):
    model = User
    form_class = LoginUserForm
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title='Вход')
        return context | base_context
    
class RegistrationView(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/registration.html'

    def get_success_url(self):
        return reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title='Регистрация')
        return context | base_context

class ShowPostView(DataMixin, DetailView):
    model = Post
    template_name = 'main/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        context['comments'] = Comment.objects.filter(post=context['post'].id)
        context['tags'] = Post.objects.get(id=context['post'].id).tags.all()
        context['form'] = AddCommentForm

        base_context = self.get_user_context(title=context['post'].title)
        return context | base_context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
        return render(request, self.template_name, self.get_context_data(user=request.user))

class CreatePostView(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title='Создание статьи')
        return context | base_context
    
    def post(self, request, *args, **kwargs):
        form = AddPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return render(request, self.template_name, self.get_context_data(**kwargs))
        
class ProfileView(DataMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'main/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title='Профиль пользователя')
        return context | base_context
    
    def get_queryset(self):
        user_posts = Post.objects.filter(author__username=self.kwargs['username'])
        return user_posts
    
class ProfileRedirectView(RedirectView):
    permanent = False
    pattern_name = 'profile'
    def get_redirect_url(self, *args: Any, **kwargs):
        user_id = self.request.user.id
        username = User.objects.get(pk=user_id).username
        return reverse('profile', kwargs={'username': username})

class SearchPostView(DataMixin, ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title='Результаты поиска')
        return context | base_context
    
    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            search_request = form.cleaned_data['title']
            self.object_list = self.get_queryset(search_request)
            return render(request, self.template_name, self.get_context_data(**kwargs))

    def get_queryset(self, search_request):
        # as icontaines doesnot work with mysql
        return Post.objects.filter(title__icontains=search_request)
    
class TagPostView(DataMixin, ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'
    slug_url_kwarg = 'tag_slug'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title=f'Посты по тэгу {self.kwargs[self.slug_url_kwarg]}')
        return context | base_context
    def get_queryset(self):
        return Post.objects.filter(tags__slug__contains=self.kwargs[self.slug_url_kwarg])
    
class ContactsView(DataMixin, View):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs: Any):
        base_context = self.get_user_context(title=f'Контакты')
        return base_context
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
