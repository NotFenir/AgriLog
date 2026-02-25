from django.urls import path

from . import views

urlpatterns = [
    path("fields/", views.FieldPage.as_view(), name="fields"),
    path("fields/<int:pk>/", views.FieldDetailPage.as_view(), name="field_detail"),
    path(
        "fields/<int:pk>/rename",
        views.FieldRenameView.as_view(),
        name="update_field_name",
    ),
    path(
        "fields/<int:pk>/add-treatment",
        views.TreatmentCreateView.as_view(),
        name="add_treatment",
    ),
    path("", views.WelcomePage.as_view(), name="dashboard"),
]
