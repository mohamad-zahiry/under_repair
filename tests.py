from django.test.testcases import TestCase
from django.test.client import Client
from django.core.cache import cache

from under_repair.middleware import UnderRepairMiddleware
from under_repair.models import UnderRepairRule, CACHE_KEY


class UnderRepairMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        cache.set(CACHE_KEY.ACTIVE, True)
        # the 0 is passed as "get_response" argument
        self.middleware = UnderRepairMiddleware(0)
        return super().setUp()

    def test_not_admin_path(self):
        response = self.client.get("")
        self.assertEquals(response.status_code, 503)

    def test_admin_path(self):
        cache.set(CACHE_KEY.ACTIVE, True)

        # default admin page
        response = self.client.get("/admin/")
        self.assertNotEqual(response.status_code, 503)

        # update admin path
        cache.set(CACHE_KEY.ADMIN, "/new_admin/")
        old_admin = self.client.get("/admin/")
        new_admin = self.client.get("/new_admin/")

        self.assertEqual(old_admin.status_code, 503)
        self.assertNotEqual(new_admin.status_code, 503)

    def test_activeness(self):
        cache.set(CACHE_KEY.ADMIN, "/admin/")
        cache.set(CACHE_KEY.ACTIVE, True)
        active_res = self.client.get("")
        cache.set(CACHE_KEY.ACTIVE, False)
        inactive_res = self.client.get("")

        self.assertEqual(active_res.status_code, 503)
        self.assertNotEqual(inactive_res.status_code, 503)

    def test_view(self):
        cache.set(CACHE_KEY.ACTIVE, True)
        cache.set(CACHE_KEY.ADMIN, "/admin/")
        cache.set(CACHE_KEY.VIEW, "wronge.view.path")
        self.client.get("")
        self.assertEqual(cache.get(CACHE_KEY.VIEW), "under_repair.views.under_repair_view")


class UnderRepairRuleTest(TestCase):
    def setUp(self) -> None:
        UnderRepairRule(description="rule 2", is_active=True).save()
        UnderRepairRule(description="rule 1", is_active=True).save()
        return super().setUp()

    def test_activate(self):
        # UnderRepairRule.activate is called each time a rule with "is_active=True" saved
        obj = UnderRepairRule.objects.get(description__exact="rule 1")
        obj.is_active = True
        obj.save()

        inactive_obj = UnderRepairRule.objects.get(is_active=False)

        self.assertEqual(obj.is_active, True)
        self.assertEqual(inactive_obj.is_active, False)

    def test_cache(self):
        rule_1 = UnderRepairRule.objects.get(description__exact="rule 1")
        rule_1.is_active = True
        rule_1.save()

        self.assertEqual(cache.get(CACHE_KEY.ACTIVE), rule_1.is_active)
        self.assertEqual(cache.get(CACHE_KEY.ADMIN), rule_1.admin_url)
        self.assertEqual(cache.get(CACHE_KEY.VIEW), rule_1.view_path)

        rules = UnderRepairRule.objects.all()
        for rule in rules:
            rule.is_active = False
            rule.save()

        self.assertEqual(cache.get(CACHE_KEY.ACTIVE), False)
