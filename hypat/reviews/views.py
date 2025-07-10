from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from .models import Review


# Allow a user to update their own review
class ReviewEdit(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ["rating", "review"]

    def get_object(self, queryset=None):
        try:
            return super().filter(user=request.user).get_object(queryset)
        except AttributeError:
            return None

    def form_valid(self, form):
        form.instance.game_id = self.kwargs["game_id"]
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)
