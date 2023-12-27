from django.contrib.sitemaps import Sitemap

from .models import MyBlog


class PostSitemap(Sitemap):
    """ни за что не поверите - это карта сайта"""

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return MyBlog.published.all()

    def lastmod(self, obj):
        return obj.updated
