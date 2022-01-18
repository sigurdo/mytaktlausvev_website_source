from os import path

from django.core.checks import Warning, register

from web.settings import BASE_DIR

DIR_SCSS = path.join(BASE_DIR, "static", "scss")


def codestyles_exist():
    """Returns `True` if both code style SCSS files exist, `False` otherwise."""
    path_default = path.join(DIR_SCSS, "codestyle-default.scss")
    path_monokai = path.join(DIR_SCSS, "codestyle-monokai.scss")
    return path.exists(path_default) and path.exists(path_monokai)


@register()
def check_codestyles_exist(app_configs, **kwargs):
    """Checks if both code style SCSS files exist."""
    if not codestyles_exist():
        return [
            Warning(
                "Missing code styles",
                hint="Code style SCSS files are missing. You might need to rerun `setup/init.sh`.",
                id="common.W001",
            )
        ]

    return []
