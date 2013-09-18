# -*- coding: utf-8 -*-
from copy import deepcopy

from django.contrib.sites.models import Site

from cms.models import Page
from cms.sitemaps import CMSSitemap
from cms.utils.i18n import get_public_languages
from cms_seoutils.i18n import get_alternate


class CMSI18nSitemap(CMSSitemap):

    def items(self):
        alt_pages = []
        site = Site.objects.get_current()
        site_languages = get_public_languages(site.pk)
        page_queryset = Page.objects.on_site(site).public()\
            .filter(login_required=False)
        for page in page_queryset:
            alt_links = get_alternate(page,
                                      site=site,
                                      site_languages=site_languages,
                                      protocol=self.protocol)
            # add alt ref to all pages
            first = True
            for lang, alt_link in alt_links.items():
                # XXX maybe redirector link should be listed as a new url?
                if alt_link['redirector']:
                    continue
                if first:
                    alt_page = deepcopy(page)
                    first = False
                else:
                    alt_page = page
                # XXX maybe alt link should only be displayed if there is
                # *more than one* alternative?
                alt_page.alternate = alt_links.values()
                # only path here: Sitemap class will add location and scheme
                alt_page._cms_i18n_absolute_url_cached = \
                    alt_links[lang]['path']
                alt_pages.append(alt_page)
        return alt_pages
    '''

            # find all public translations for this page
            available_languages = {l for l in page.get_languages()
                                   if l in site_languages}
            sitemap_languages = [l for l in site_languages
                                 if l in available_languages]

            # handle case when hide_untranslated = False
            if len(sitemap_languages) < len(site_languages):
                for lang in site_languages:
                    if (lang not in sitemap_languages
                        and not hide_untranslated(lang, site_id)):
                        for fb_lang in sitemap_languages:
                            if fb_lang in get_fallback_languages(lang,
                                                                 site_id):
                                sitemap_languages.append(lang)
                                break
            # cache absolute url by language
            alt_urls = OrderedDict()
            for lang in sitemap_languages:
                with override(lang):
                    alt_urls[lang] = page.get_absolute_url()

            assert len(alt_urls) == len(set(alt_urls.values())), \
                'duplicate url found: %s' % alt_urls

            # add redirecting default url
            if alt_urls:
                url = list(urlparse.urlparse(alt_urls[lang]))
                url[2] = re.sub(r'^/{}'.format(lang), '', url[2])
                alt_urls['x-default'] = urlparse.urlunparse(url)
                # XXX should we add x-default to the sitemap???
                #sitemap_languages.append('x-default')

            # alternate link objects
            alt_links = [{'language_code': lang,
                          'location': '%s://%s%s' % (protocol, domain, url)}
                         for lang, url in alt_urls.items()]

            # add alt ref to all pages
            for i, lang in enumerate(sitemap_languages):
                alt_page = deepcopy(page) if i else page
                if len(alt_links) > 1:
                    alt_page.alternate = alt_links
                alt_page._cms_i18n_absolute_url_cached = alt_urls[lang]
                alt_pages.append(alt_page)

        return alt_pages
    '''

    def location(self, obj):
        return obj._cms_i18n_absolute_url_cached
