from django.urls import path

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Game

from .views import GameListView, ReleaseListView

app_name = "games"
urlpatterns = [
    path("<int:game_id>/releases/", ReleaseListView.as_view(), name="release_list"),
    #path("<int:pk>/", DetailView.as_view(model=Game), name="game_detail"),
    path("<int:pk>/", DetailView.as_view(queryset=Game.objects.select_related("primary")), name="game_detail"),
    #path(
    #    "",
    #    ListView.as_view(
    #        queryset=Game.objects.prefetch_related("release_set"), paginate_by=100
    #    ),
    #    name="game_list",
    #),
    path("", GameListView.as_view(), name="game_list"),
]
