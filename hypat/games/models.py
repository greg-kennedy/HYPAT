from django.db import models


class Game(models.Model):
    name = models.CharField(
        max_length=255, unique=True, help_text="Name of the game group"
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

        return reverse("games:game_detail", args=[str(self.pk)])

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Release(models.Model):
    class Region(models.TextChoices):
        NTSC = "N", "NTSC"
        PAL = "P", "PAL"
        SECAM = "S", "SECAM"

    class Controller(models.TextChoices):
        JOYSTICK = "JS", "Joystick"
        TRON = "TJ", "TRON Joystick"
        KID = "KC", "Kid's Controller"
        PADDLE = "PD", "Paddle"
        KEYBOARD = "KB", "Keyboard Controller"
        KIDVID = "KV", "Kid Vid Voice Module"
        MINDLINK = "ML", "Mindlink Controller"
        DRIVING = "DC", "Driving Controller"
        JOYBOARD = "JB", "Joyboard"
        BOOSTER = "BG", "Booster Grip"
        LIGHTGUN = "LG", "Light Gun"
        DUAL = "DM", "Dual Control Module"
        TOUCH = "TP", "Video Touch Pad"
        TRACK_FIELD = "TF", "Track & Field Controller"
        BIKE = "BT", "Bike Trainer"

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    rom = models.FileField(max_length=255)
    image = models.ImageField(max_length=255)

    name = models.CharField(max_length=255)
    alt = models.CharField(max_length=255, blank=True)
    aka = models.CharField(max_length=255, blank=True)
    beta = models.CharField(max_length=255, blank=True)
    year = models.CharField(max_length=255, blank=True)
    mfg = models.CharField(max_length=255, blank=True)
    serial = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=1, choices = Region, default = Region.NTSC)
    controller = models.CharField(max_length=2, choices = Controller, default = Controller.JOYSTICK)
    comp = models.CharField(max_length=255, blank=True)
    disam = models.CharField(max_length=255, blank=True)
    multi = models.CharField(max_length=255, blank=True)

    url = models.URLField(max_length=255, blank=True)
    note = models.TextField(blank=True)

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
