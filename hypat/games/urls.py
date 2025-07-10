from django.urls import path
from django.views.generic.detail import DetailView

from .models import Game
from .views import GameListView, ReleaseListView

app_name = "games"
urlpatterns = [
    path("<int:game_id>/releases/", ReleaseListView.as_view(), name="release_list"),
    path("<int:pk>/", DetailView.as_view(queryset=Game.objects.select_related("primary")), name="game_detail"),
    path("", GameListView.as_view(), name="game_list"),
]
