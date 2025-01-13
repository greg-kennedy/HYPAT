from django.shortcuts import get_object_or_404

from django.views.generic.list import ListView

from .models import Game, Release

# Create your views here.

class ReleaseListView(ListView):
    model = Release

    def get_queryset(self):
        self.game = get_object_or_404(Game, id=self.kwargs["game_id"])
        return Release.objects.filter(game = self.game)
