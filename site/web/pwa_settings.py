import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PWA_APP_NAME = "Taktlausveven"
PWA_APP_DESCRIPTION = "Heimvevstaden til studentorchesteret dei taktlause"
PWA_APP_THEME_COLOR = "#a50104"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_ORIENTATION = "portrait"
PWA_APP_ICONS = [
    {
        "src": "/static/images/logo.svg",
    },
    {
        "src": "/static/images/logo_256x256.png",
        "sizes": "256x256",
        "purpose": "any",
    }
]
PWA_APP_ICONS_APPLE = [
    {
        "src": "/static/images/logo.svg",
    },
    {
        "src": "/static/images/logo_256x256.png",
        "sizes": "256x256",
        "purpose": "any",
    }
]
PWA_APP_DIR = "pwa"
PWA_APP_LANG = "nn-no"
PWA_APP_START_URL = "/"
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "static", "js", "serviceworker.js")
