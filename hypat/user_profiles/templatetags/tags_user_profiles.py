from django import template

from django.contrib.auth.models import User

register = template.Library()


@register.inclusion_tag("user_profiles/tag_user.html")
def user(pk):
    """Renders a User for presentation, giving a link to their profile page and a class for icon"""
    if pk:
        try:
            object = User.objects.get(pk=pk)
            type = (
                "superuser"
                if object.is_superuser
                else "staff" if object.is_staff else "user"
            )
            return {
                "id": pk,
                "username": object.get_username(),
                "type": type,
                "is_active": object.is_active,
            }
        except User.DoesNotExist:
            return {"id": pk, "type": none}

    return {"id": pk, "type": none}
