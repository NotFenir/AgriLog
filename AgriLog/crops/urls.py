from django.urls import path

from . import views

urlpatterns = [
    path("fields/", views.FieldPage.as_view(), name="fields"),
    path("", views.WelcomePage.as_view(), name="dashboard"),
]
