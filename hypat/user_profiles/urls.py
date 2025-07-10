from django.urls import path
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Profile
from .views import ProfileUpdate

app_name = "user_profiles"

urlpatterns = [
    path("<int:pk>/update/", ProfileUpdate.as_view(), name="profile_update"),
    path("<int:pk>/", DetailView.as_view(model=Profile), name="profile_detail"),
    path("", ListView.as_view(model=Profile, paginate_by=100), name="profile_list"),
]
