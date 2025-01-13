from django.urls import path

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Review

from .views import ReviewEdit

app_name = "reviews"
urlpatterns = [
    path("<int:game_id>/edit", ReviewEdit.as_view(), name="review_edit"),
    path("<int:pk>", DetailView.as_view(model=Review), name="review_update"),
    path("", ListView.as_view(model=Review, paginate_by=100), name="review_list"),
]
