from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import FormMixin

from .forms import (
    CultivationEditForm,
    CultivationNotesForm,
    FieldEditForm,
    FieldNotesForm,
    TreatmentAddForm,
)
from .models import CropType, Cultivation, Field, Treatment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "treatment_form" not in context:
            context["treatment_form"] = TreatmentAddForm()

        return context


class FieldEditView(LoginRequiredMixin, UpdateView):
    model = Field
    form_class = FieldEditForm

    def get_success_url(self):
        return reverse_lazy("field_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zaktualizowano dane pola")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect("field_detail", pk=self.kwargs["pk"])


class TreatmentCreateView(LoginRequiredMixin, CreateView):
    model = Treatment
    form_class = TreatmentAddForm

    def form_valid(self, form):
        field_id = self.kwargs.get("pk")
        field = get_object_or_404(Field, id=field_id, owner=self.request.user)

        form.instance.field = field
        messages.success(self.request, "Zabieg został dodany pomyślnie")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("field_detail", kwargs={"pk": self.kwargs.get("pk")})


class CultivationsHistoryView(LoginRequiredMixin, ListView):
    model = Cultivation
    template_name = "panels/cultivation_history.html"
    context_object_name = "cultivations_list"
    paginate_by = 25

    def get_queryset(self):
        return (
            Cultivation.objects.filter(owner=self.request.user)
            .select_related("field", "crop_type")
            .order_by("-year", "-created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_crops"] = CropType.objects.all()
        context["user_fields"] = Field.objects.filter(owner=self.request.user)
        return context


class CultivationDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Cultivation
    template_name = "details/cultivation_detail.html"
    context_object_name = "cultivation"
    form_class = CultivationNotesForm

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
        cultivation = self.get_object()
        cultivation.notes = form.cleaned_data["notes"]
        cultivation.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_form"] = CultivationEditForm(instance=self.get_object())
        return context


class CultivationEditView(LoginRequiredMixin, UpdateView):
    model = Cultivation
    form_class = CultivationEditForm

    def get_success_url(self):
        return reverse_lazy("cultivation_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zaktualizowano dane uprawy")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect("cultivation_detail", pk=self.kwargs["pk"])
