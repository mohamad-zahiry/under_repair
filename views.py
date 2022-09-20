from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site


def under_repair_view(request, *args, **kwargs):
    site = get_current_site(request)
    context = {"title": "Sorry :(", "domain": site}
    return render(request, "under_repair/index.html", context=context)
