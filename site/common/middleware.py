from django.contrib.redirects.middleware import (
    RedirectFallbackMiddleware as BaseRedirectFallbackMiddleware,
)
from django.http import HttpResponseRedirect


class RedirectFallbackMiddleware(BaseRedirectFallbackMiddleware):
    """`RedirectFallbackMiddleware` overriden to return a temporary redirect."""

    response_redirect_class = HttpResponseRedirect
