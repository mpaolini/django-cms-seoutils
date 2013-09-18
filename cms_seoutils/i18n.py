from __future__ import absolute_import

import re
from collections import OrderedDict

from django.contrib.sites.models import Site
from django.utils.translation import override

from cms.utils.i18n import (get_public_languages, get_fallback_languages,
                            hide_untranslated)
from .config import get_config_redirectors

LANG_REDIRECTOR = 'x-default'


def get_alternate(page, site=None, site_languages=None, protocol=None,
                  enable_redirectors=None):
    # Optimize for repeated calls within the same site
    if site is None:
        site = Site.objects.get_current()
    if site_languages is None:
        site_languages = get_public_languages(site.pk)
    # TODO: build API for this default
    if enable_redirectors is None:
       enable_redirectors = get_config_redirectors()

    protocol = protocol if protocol is not None else 'http'

    # find all public translations for this page
    available_languages = {l for l in page.get_languages()
                           if l in site_languages}
    sitemap_languages = [l for l in site_languages
                         if l in available_languages]

    # handle case when hide_untranslated = False
    if len(sitemap_languages) < len(site_languages):
        for lang in site_languages:
            if (lang not in sitemap_languages
                and not hide_untranslated(lang, site.pk)):
                for fb_lang in sitemap_languages:
                    if fb_lang in get_fallback_languages(lang, site.pk):
                        sitemap_languages.append(lang)
                        break

    # Append default redirector link
    if sitemap_languages and enable_redirectors:
        sitemap_languages.append(LANG_REDIRECTOR)

    alt_links = OrderedDict()

    for lang in sitemap_languages:
        if lang == LANG_REDIRECTOR:
            with override(sitemap_languages[0]):
                url = page.get_absolute_url()
            url = re.sub(r'^/{}'.format(sitemap_languages[0]), '', url)
            assert sitemap_languages[0] != LANG_REDIRECTOR
        else:
            with override(lang):
                url = page.get_absolute_url()
        alt_links[lang] = {'language_code': lang,
                           'location': '%s://%s%s' % (protocol,
                                                      site.domain,
                                                      url),
                           'redirector': lang == LANG_REDIRECTOR,
                           'path': url}
    return alt_links
