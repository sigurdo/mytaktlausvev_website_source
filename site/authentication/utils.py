from django.contrib.auth.models import Permission


def find_permission_instance(permission_string):
    """
    Tries to find a permission instance from a string on the format "<app label>.<codename>".
    Returns None if the permission was not found.
    """
    app_label, codename = permission_string.split(".")
    queryset = Permission.objects.filter(
        codename=codename, content_type__app_label=app_label
    )
    if not queryset.exists():
        return None
    return queryset.first()
