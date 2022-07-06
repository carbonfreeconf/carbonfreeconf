from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return ['my_app:home','my_app:about','my_app:register'
            ,'my_app:archive','my_app:news','my_app:conf','my_app:pricing','my_app:tutorial'
            ,'my_app:legalnotice','my_app:contactform','my_app:faq','my_app:hostconf','blog:bloghome']
    def location(self, item):
        return reverse(item)

