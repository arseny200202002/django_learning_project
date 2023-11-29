from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',                        views.HomeView.as_view(), name='home'),
    path('about/',                  views.AboutView.as_view(), name='about'),
    path('contacts/',               views.ContactsView.as_view(), name='contacts'),

    path('login/',                  views.LoginUserView.as_view(), name='login'),
    path('registartion/',           views.RegistrationView.as_view(), name='registration'),
    path('logout/',                 LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),

    path('create_post/',            views.CreatePostView.as_view(), name='create_post'),
    path('post/<slug:post_slug>/',  views.ShowPostView.as_view(), name='post'),
    path('tag/<slug:tag_slug>/',   views.TagPostView.as_view(), name='tag'),
    path('profile/<slug:username>/',views.ProfileView.as_view(), name='profile'),
    
    path('my_profile/',             views.ProfileRedirectView.as_view(), name='my_profile'),
    path('search/',                 views.SearchPostView.as_view(), name='search')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
