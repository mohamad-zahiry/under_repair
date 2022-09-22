from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sites.shortcuts import get_current_site


DEFAULTS = {
    "ACTIVATE": False,
    "VIEW": "under_repair.views.under_repair_view",
}

UNDER_REPAIR = getattr(settings, "UNDER_REPAIR", DEFAULTS)


def _is_activated():
    return UNDER_REPAIR.get("ACTIVATE", DEFAULTS["ACTIVATE"])


def _get_view():
    path = UNDER_REPAIR.get("VIEW", DEFAULTS["VIEW"]).split(".")
    view = path[-1]
    module = __import__(".".join(path[:-1]), globals(), locals(), [view], 0)
    return getattr(module, view)


class UnderRepairMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

        self.activated = _is_activated()
        self.view = _get_view()

    def process_request(self, request):
        ADMIN_PAGE = UNDER_REPAIR.get("ADMIN_PAGE", f"{get_current_site(request)}/admin").rstrip("/")
        CURRENT_URL = f"{get_current_site(request)}{request.path_info}"

        if self.activated and not (ADMIN_PAGE in CURRENT_URL):
            response = self.view(request)
            if response.status_code != 503:
                raise Exception("The status code must be 503")
            return response
