from .models import *
from .forms import SearchForm

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Контакты', 'url_name': 'contacts'},
]

guest_submenu = [
    {'title': 'Войти', 'url_name': 'login'},
    {'title': 'Регистрация', 'url_name': 'registration'},
]

user_submenu = [
    {'title': 'Профиль', 'url_name': 'my_profile'},
    {'title': 'Добавить статью', 'url_name': 'create_post'},
    {'title': 'Выход', 'url_name': 'logout'},
]

search_form = SearchForm()

class DataMixin():
    paginate_by = 10

    def get_user_context(self, *args, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            context['submenu'] = user_submenu 
        else:
            context['submenu'] = guest_submenu

        context['menu'] = menu
        context['search_form'] = search_form
        return context