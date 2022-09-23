from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache

from .models import CACHE_KEY, _update_cache


DEFAULTS = {
    "ACTIVATE": False,
    "VIEW": "under_repair.views.under_repair_view",
}

UNDER_REPAIR = getattr(settings, "UNDER_REPAIR", DEFAULTS)


def _is_activated():
    return cache.get(CACHE_KEY.ACTIVE)


def _parse_view_path(dot_path):
    path = dot_path.split(".")
    module = ".".join(path[:-1])
    view = path[-1]
    return (module, view)


def _get_view():
    view_path = cache.get(CACHE_KEY.VIEW, DEFAULTS["VIEW"])
    module, view_name = _parse_view_path(view_path)
    try:
        module = __import__(module, globals(), locals(), [view_name], 0)
        view = getattr(module, view_name)
    except ModuleNotFoundError:
        print(f"[UnderRepair]: module '{module}' not found")
    except AttributeError:
        print(f"[UnderRepair]: module {module} does not have '{view_name}' function")
    else:
        return view

    cache.set(CACHE_KEY.VIEW, DEFAULTS["VIEW"])
    module, view_name = _parse_view_path(DEFAULTS["VIEW"])
    module = __import__(module, globals(), locals(), [view_name], 0)
    return getattr(module, view_name)


def _get_admin(request):
    return cache.get(CACHE_KEY.ADMIN, f"{get_current_site(request)}/admin").rstrip("/")


def _get_current_url(request):
    return f"{get_current_site(request)}{request.path_info}"


class UnderRepairMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

        # check cache setup. if _is_activated returns None, the cache is not setup
        if _is_activated() is None:
            _update_cache()

    def process_request(self, request):
        is_active = _is_activated()
        view = _get_view()
        admin_url = _get_admin(request)
        current_url = _get_current_url(request)

        if is_active and not (admin_url in current_url):
            response = view(request)
            if response.status_code != 503:
                raise Exception("The status code must be 503")
            return response
