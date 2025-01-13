from django.contrib import admin
from hypat.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "game_name", "rating", "review")
