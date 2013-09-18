from django.conf.urls import url, patterns, include
from django.contrib.admin import site
from django.conf.urls.i18n import i18n_patterns

from cms_seoutils.sitemaps import CMSI18nSitemap


urlpatterns = patterns(
    '',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSI18nSitemap}}, name='sitemap'),
    url(r'^admin/', include(site.urls)),
)


urlpatterns += i18n_patterns(
    '',
    url(r'^', include('cms.urls')),
)
