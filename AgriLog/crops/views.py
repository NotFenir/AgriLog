from django.views.generic import TemplateView, DetailView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Field
from .forms import FieldNotesForm, FieldRenameForm


class UserObjectMixin(LoginRequiredMixin):
    def get_object(self):
        return self.request.user


class WelcomePage(LoginRequiredMixin, TemplateView):
    template_name = "panels/dashboard.html"


class FieldPage(UserObjectMixin, TemplateView):
    template_name = "panels/fields.html"


class FieldDetailPage(LoginRequiredMixin, FormMixin, DetailView):
    model = Field
    template_name = "details/field_detail.html"
    context_object_name = "field"
    form_class = FieldNotesForm

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        field = self.get_object()
        field.notes = form.cleaned_data["notes"]
        field.save()
        return super().form_valid(form)


class FieldRenameView(LoginRequiredMixin, UpdateView):
    model = Field
    form_class = FieldRenameForm

    def get_success_url(self):
        return reverse_lazy("field_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zmieniono nazwę pola")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect("field_detail", pk=self.kwargs["pk"])
