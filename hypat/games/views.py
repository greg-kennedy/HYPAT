from django.shortcuts import get_object_or_404

from django.views.generic.list import ListView

from .models import Game, Release

# Create your views here.


class ReleaseListView(ListView):
    model = Release

    def get_queryset(self):
        self.game = get_object_or_404(Game, id=self.kwargs["game_id"])
        return super().get_queryset().filter(game=self.game)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = self.game
        return context

class GameListView(ListView):
    model = Game
    paginate_by=100

    def get_queryset(self):
        # base qs
        qs = super().get_queryset()

        # add optional filtering and order
        if self.request.GET.get("canonical"):
            qs = qs.filter(is_canon=self.request.GET.get("canonical"))

        if self.request.GET.get("order"):
            qs = qs.order_by(self.request.GET.get("order"))

        return qs.select_related("primary")
