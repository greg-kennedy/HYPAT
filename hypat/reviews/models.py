from django.db import models

from django.utils.functional import cached_property
from django.contrib.auth.models import User

from ..games.models import Game


# Create your models here.
class Review(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #pk = models.CompositePrimaryKey("game", "user")

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    rating = models.PositiveSmallIntegerField(blank=True)
    review = models.TextField(blank=True)

    @cached_property
    def user_name(self):
        return self.user.username

    @cached_property
    def game_name(self):
        return self.game.name

    class Meta:
        ordering = ["game", "user"]
        unique_together = ["game", "user"]

    def __str__(self):
        return f"{self.user.username}: {self.game.name} = {self.rating}"
