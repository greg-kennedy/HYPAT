from django.contrib import admin
from django.forms import ModelForm
from hypat.games.models import Game, Release


class ReleaseInlineAdmin(admin.TabularInline):
    model = Release
    fields = ["id", "name", "mfg", "beta", "region"]
    readonly_fields = ["name", "mfg", "beta", "region"]
    show_change_link = True
    max_num = 1


class GameAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["primary"].queryset = self.instance.release_set.all()

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    #list_display = ["id", "is_canon", "name", "release_count"]
    #list_filter = ["is_canon"]
    #list_editable = ["is_canon"]
    inlines = [ReleaseInlineAdmin]
    form = GameAdminForm


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "name", "beta", "mfg")
