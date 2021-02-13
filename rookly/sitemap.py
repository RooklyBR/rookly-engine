import re

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from rookly.common.models import BusinessService


class ServicesViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def get_urls(self, site=None, **kwargs):
        site.domain = re.sub(
            r"https://www\.|http://www\.|https://www|http://|https://|www\.",
            "",
            settings.ROOKLY_WEBAPP_BASE_URL,
        ).strip("/")
        return super(ServicesViewSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return BusinessService.objects.all()[:100].values_list("pk", flat=True)

    def location(self, item):
        return f"/Prestador/{item}/"

    def lastmod(self, item):
        return timezone.now()
