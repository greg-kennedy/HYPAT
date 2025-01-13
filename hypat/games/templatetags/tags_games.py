from django import template

from ..models import Game, Release

register = template.Library()

@register.inclusion_tag('games/tag_game.html')
def game(game_id):
    """
    Display a Game ID as a link and CSS class.

    Sample usage:

        {% game [id] %}

    This retrieves the game by ``ID`` and creates a link to their detail page, using the game name as the link text.  The link has a unique class (``game``) so it can be styled separately.
    """
    if game_id:
        try:
            object = Game.objects.get(pk=game_id)
            return { 'game_id': object.pk, 'enabled': object.enabled, 'name': object.name }
        except Game.DoesNotExist:
            return { 'game_id': game_id }

    return { 'game_id': 0 }

@register.inclusion_tag('games/tag_release.html')
def release(release_id):
    """
    Display a Release ID as a link and CSS class.

    Sample usage:

        {% release [id] %}

    This retrieves the release by ``ID`` and creates a link to their detail page, using the release name as the link text.  The link has a unique class (``release``) so it can be styled separately.
    """
    if release_id:
        try:
            object = Release.objects.get(pk=release_id)
            return { 'game_id': object.game.pk, 'release_id': object.pk, 'primary': object.primary, 'name': object.name }
        except Release.DoesNotExist:
            return { 'release_id': release_id, }

    return { 'release_id': 0 }
