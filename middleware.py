from django.conf import settings
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class UnderRepairMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if getattr(settings, "SITE_UNDER_REPAIR", False):
            return HttpResponse("This site is under repaire. Come back later")
