from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .forms import EmailRegistrationForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "account/register.html"
    form_class = EmailRegistrationForm
    success_url = reverse_lazy("login")
    success_message = "Konto zostało utworzone pomyślnie!"


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "account/profile.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user
