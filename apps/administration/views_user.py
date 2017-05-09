from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView
from apps.administration.components.form_user import UserForm


class UserCreate(CreateView):
    model = User
    template_name = "administration/user/usersCreate.html"
    form_class = UserForm
    success_url = reverse_lazy('user')

class UserView(ListView):
    model = User
    template_name = 'administration/user/usersView.html'