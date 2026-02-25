from django.urls import path

from . import views

urlpatterns = [
    path("fields/", views.FieldPage.as_view(), name="fields"),
    path("fields/<pk>/", views.FieldDetailPage.as_view(), name="field_detail"),
    path("", views.WelcomePage.as_view(), name="dashboard"),
]
