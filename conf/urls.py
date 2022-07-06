"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from my_app import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from my_app.sitemaps import StaticViewSitemap
from my_app.models import Post, Website
from post.models import Post as Post2
from django.conf.urls.i18n import i18n_patterns

#sitemaps = {
#    'static': StaticViewSitemap
#}

sitemaps = {
    'my_app:news': GenericSitemap({
        'queryset': Post.objects.filter(status=1),
        'date_field': 'updated_on',
    }, priority=0.9),
    'blog:post': GenericSitemap({
        'queryset': Post2.objects.filter(),
        'date_field': 'timestamp',
    }, priority=0.9),
    #'my_app:website': GenericSitemap({
    #    'queryset': Website.objects.all(),
    #    'date_field': 'updated_on',
    #}, priority=0.7),
    # START
    'static': StaticViewSitemap,
    # END
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('my_app.urls', namespace="my_app")),
    path('', include('blog.urls')),
    path('', include('qa.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('admin/statuscheck/', include('celerybeat_status.urls')),
    path('special', views.special, name='special'),
    path('logout', views.user_logout, name='logout'),
    path('tz_detect',include('tz_detect.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('captcha/', include('captcha.urls')),
#    path('tellme/', include("tellme.urls")),
    path('cookies/', include('cookie_consent.urls'))

]
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

urlpatterns += i18n_patterns (
    path('',include('my_app.urls', namespace="my_app2")),
    path('',include('blog.urls', namespace="blog2")),
)



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


