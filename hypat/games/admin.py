from django.contrib import admin
from hypat.games.models import Game, Release

class ReleaseInlineAdmin(admin.TabularInline):
    model = Release
    fields = [ "id", "primary", "name", "mfg", "beta", "region" ]
    readonly_fields = [ "name", "mfg", "beta", "region" ]
    show_change_link = True
    max_num = 1

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "enabled", "name", "release_count"]
    list_filter = ["enabled"]
    list_editable = ["enabled"]
    inlines = [ ReleaseInlineAdmin ]

@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "primary", "name", "beta", "mfg")
