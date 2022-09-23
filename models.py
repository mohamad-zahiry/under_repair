from django.db import models
from django.core.cache import cache
from django.db.models import Q


class CACHE_KEY:
    ACTIVE = "under_repair-is_active"
    ADMIN = "under_repair-admin_url"
    VIEW = "under_repair-view_path"


class UnderRepairRule(models.Model):
    description = models.CharField(
        max_length=200,
        help_text="A short desctription about the rule",
    )
    is_active = models.BooleanField(default=False, help_text="Status of the rule")
    admin_url = models.CharField(
        max_length=200,
        default="127.0.0.1:8000/admin",
        blank=False,
        null=False,
        help_text="The admin page url without protocol and www.\ne.g: yahoo.com/admin",
    )
    view_path = models.CharField(
        default="under_repair.views.under_repair_view",
        max_length=200,
        help_text="Absolute path to your view.\ne.g: PROJECT_ROOT.APP.views.VIEW_NAME",
    )

    class Meta:
        verbose_name = "Under Repair Rule"
        verbose_name_plural = "Under Repair Rules"

    def save(self, *args, **kwargs):
        if self.is_active:
            self.acitvate(self)
        super().save(*args, **kwargs)
        _update_cache()

    def __str__(self) -> str:
        status = "Activated" if self.is_active else "Deactivated"
        return f"[{status}] {self.description}"

    @classmethod
    def acitvate(cls, obj):
        qs = cls.objects.filter(~Q(description=obj.description) & Q(is_active=True))
        qs.update(is_active=False)


def _update_cache():
    qs = UnderRepairRule.objects.filter(is_active=True)
    if qs.exists():
        obj = qs.first()
        cache.set(CACHE_KEY.ACTIVE, True)
        cache.set(CACHE_KEY.ADMIN, obj.admin_url)
        cache.set(CACHE_KEY.VIEW, obj.view_path)
    else:
        cache.set(CACHE_KEY.ACTIVE, False)
