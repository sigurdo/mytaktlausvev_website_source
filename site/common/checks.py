from os import path, scandir

from django.core.checks import Warning, register

from web.settings import BASE_DIR

DIR_SCSS = path.join(BASE_DIR, "static", "scss")


def codestyles_exist() -> bool:
    """Returns `True` if both code style SCSS files exist, `False` otherwise."""
    path_default = path.join(DIR_SCSS, "codestyle-default.scss")
    path_monokai = path.join(DIR_SCSS, "codestyle-monokai.scss")
    return path.exists(path_default) and path.exists(path_monokai)


def submodule_cloned(path_submodule: str) -> bool:
    """
    Returns `True` if the submodule at
    `path_submodule` has been cloned, `False` otherwise.

    Assumes that a submodule has been cloned if
    the directory at `path_submodule` exists and is not empty.
    """
    return path.isdir(path_submodule) and any(scandir(path_submodule))


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


@register()
def check_submodules_cloned(app_configs, **kwargs):
    """Checks if submodules `bootstrap` and `bootswatch` have been cloned."""
    submodules_cloned = submodule_cloned(
        path.join(DIR_SCSS, "bootstrap")
    ) and submodule_cloned(path.join(DIR_SCSS, "bootswatch"))
    if not submodules_cloned:
        return [
            Warning(
                "Submodules not cloned.",
                hint=(
                    "Submodules have not been cloned. "
                    "They can be cloned by running "
                    "`git submodule update --init --recursive`."
                ),
                id="common.W002",
            )
        ]

    return []
