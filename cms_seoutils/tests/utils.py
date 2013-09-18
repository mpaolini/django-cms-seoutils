'''
Utilities for tests.
'''
from cms.utils.conf import get_languages
from cms.test_utils.testcases import CMSTestCase

from cms.api import create_page, publish_page

from django.contrib.sites.models import Site


def merge_dict(a, b):
    for k, v in b.iteritems():
        if k in a and isinstance(a[k], list) and isinstance(v, list):
            # merge the two list of dicts
            a_k = []
            b_code = {d['code']: d for d in v}
            for a_d in a[k]:
                b_d = b_code.pop(a_d['code'], None)
                if b_d is None:
                    a_k.append(a_d)
                else:
                    a_k.append(merge_dict(a_d, b_d))
            a_k.extend(b_d for b_d in v if b_d['code'] in b_code)
            a[k] = a_k
        elif k in a and isinstance(a[k], dict):
            a[k] = merge_dict(a[k], v)
        else:
            a[k] = v
    return a


def get_cms_languages(opts):
    return merge_dict(get_languages(), opts)


class SEOUtilsTestCase(CMSTestCase):

    urls = 'cms_seoutils.test_utils.project.urls'

    def create_page(self, language=None, site=None, published=True,
                    template='empty.html'):
        if site is None:
            site = Site.objects.get_current()
        if language is None:
            language = 'en'
        page_data = self.get_new_page_data_dbfields(
            site=site,
            language=language,
            template=template,
        )
        page = create_page(**page_data)
        if published:
            user = self.get_superuser()
            publish_page(page, user)
        return page

    def get_url(self, path, site=None):
        if site is None:
            site = Site.objects.get_current()
        return 'http://{}{}'.format(site.domain, path)
