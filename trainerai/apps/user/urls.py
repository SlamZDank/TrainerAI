from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.ProfileCreateView.as_view()),
]
