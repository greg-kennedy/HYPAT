from django.db import models

from django.utils.functional import cached_property


# Create your models here.
class Game(models.Model):

    name = models.CharField(
        max_length=191, unique=True, help_text="Name of the game group"
    )

    is_canon = models.BooleanField(
        help_text="Whether or not the game should count towards Completion"
    )

    description = models.TextField(
        blank=True, help_text="Free-form HTML text about the game"
    )

    primary = models.OneToOneField(
        "Release",
        related_name="primary",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Primary Release associated with this Game",
    )

    # @cached_property
    # def release_count(self):
    #    return self.release_set.count()

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("games:game_detail", args=[str(self.id)])

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Release(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    rom = models.FileField(max_length=255)
    image = models.ImageField(max_length=255)

    name = models.CharField(max_length=255, blank=False)
    alt = models.CharField(max_length=255)
    aka = models.CharField(max_length=255)
    beta = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    mfg = models.CharField(max_length=255)
    serial = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    controller = models.CharField(max_length=255)
    comp = models.CharField(max_length=255)
    disam = models.CharField(max_length=255)
    multi = models.CharField(max_length=255)

    url = models.CharField(max_length=255)
    note = models.TextField()

    class Meta:
        unique_together = (
            "game",
            "name",
            "alt",
            "aka",
            "beta",
            "year",
            "mfg",
            "region",
            "controller",
            "comp",
            "disam",
            "multi",
        )
        # ordering = ["-primary", "id"]

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("games:release_list", args=[str(self.game.id)])

    def __str__(self):
        return f"{self.name} - {self.mfg} ({self.region}, {self.beta}, {self.disam})"
