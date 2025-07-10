from django.urls import path
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Review
from .views import ReviewEdit

app_name = "reviews"
urlpatterns = [
    path("game/<int:game_id>/edit", ReviewEdit.as_view(), name="review_edit"),
    path("game/<int:game_id>", ListView.as_view(model=Review, paginate_by=100), name="review_game_list"),
    path("user/<int:user_id>", ListView.as_view(model=Review, paginate_by=100), name="review_user_list"),
    path("<int:pk>", DetailView.as_view(model=Review), name="review_update"),
]
