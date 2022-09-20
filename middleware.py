from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


DEFAULTS = {
    "ACTIVATE": False,
    "VIEW": ".views.under_repair_view",
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
        if self.activated:
            return self.view(request)
