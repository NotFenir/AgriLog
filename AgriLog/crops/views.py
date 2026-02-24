from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class WelcomePage(LoginRequiredMixin, TemplateView):
    template_name = "panels/dashboard.html"


class FieldPage(LoginRequiredMixin, TemplateView):
    template_name = "panels/fields.html"
