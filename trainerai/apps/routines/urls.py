from django.urls import path
from . import views

urlpatterns = [
    path("routines/", views.RoutineListCreateView.as_view(), name="routines-list"),
    path("routines/<uuid:routine_id>/", views.RoutineDetailView.as_view(), name="routine-detail"),
    path("routines/user/<uuid:user_id>/", views.UserRoutineListView.as_view(), name="user-routines-list"),
]