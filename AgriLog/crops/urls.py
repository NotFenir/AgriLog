from django.urls import path

from . import views

urlpatterns = [
    path("fields/", views.FieldPage.as_view(), name="fields"),
    path("fields/<int:pk>/", views.FieldDetailPage.as_view(), name="field_detail"),
    path(
        "fields/<int:pk>/update",
        views.FieldEditView.as_view(),
        name="update_field",
    ),
    path(
        "fields/<int:pk>/add-treatment",
        views.TreatmentCreateView.as_view(),
        name="add_treatment",
    ),
    path(
        "cultivations/",
        views.CultivationsHistoryView.as_view(),
        name="cultivations",
    ),
    path(
        "cultivations/<int:pk>/",
        views.CultivationDetailView.as_view(),
        name="cultivation_detail",
    ),
    path(
        "cultivations/<int:pk>/update",
        views.CultivationEditView.as_view(),
        name="update_cultivation",
    ),
    path("", views.WelcomePage.as_view(), name="dashboard"),
]
