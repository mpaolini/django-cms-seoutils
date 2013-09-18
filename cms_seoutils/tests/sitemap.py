from lxml import etree

from cms.api import create_title, publish_page

from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from cms_seoutils.tests.utils import get_cms_languages, SEOUtilsTestCase


class SitemapTestCase(SEOUtilsTestCase):

    urls = 'cms_seoutils.test_utils.project.urls'

    def get_sitemap(self, **opts):
        resp = self.client.get(reverse('sitemap'), **opts)
        self.assertEqual(resp.status_code, 200)
        return etree.fromstring(resp.content)

    def test_empty(self):
        elem = self.get_sitemap()
        self.assertFalse(list(elem))

    def test_one_page_en_unpublished(self):
        page = self.create_page(language='en', published=False)
        elem = self.get_sitemap()
        self.assertFalse(list(elem))

    def test_one_page_en(self):
        from cms.models import Page
        self.assertEqual(Page.objects.published().count(), 0)
        page = self.create_page(language='en')
        elem = self.get_sitemap()
        self.assertEqual(len(list(elem)), 1)
        self.assertEqual(elem.find('{*}url/{*}loc').text,
                         self.get_url('/en/'))
        # Act like a crawler: check the page
        resp = self.client.get('/en/')
        self.assertEqual(resp.status_code, 200)

    @override_settings(CMS_LANGUAGES=get_cms_languages(
            {1: [{'code': 'it', 'hide_untranslated': False}]}))
    def test_one_page_en_show_untranslated(self):
        from cms.utils.conf import get_languages
        page = self.create_page(language='en')
        elem = self.get_sitemap()
        self.assertEqual(len(list(elem)), 2)
        self.assertEqual([e.text for e in elem.findall('{*}url/{*}loc')],
                         [self.get_url('/en/'), self.get_url('/it/')])
        links = [e.attrib for e in elem.find('{*}url').findall('{*}link')]
        self.assertEquals(
            links,
            [{'rel': 'alternate', 'hreflang': lang,
              'href': self.get_url(url)}
             for lang, url in (('en', '/en/'), ('it', '/it/'))])

    def test_one_page_en_request_it(self):
        page = self.create_page(language='en')
        elem = self.get_sitemap(HTTP_ACCEPT_LANGUAGE='it')
        self.assertEqual(len(list(elem)), 1)
        self.assertEqual(elem.find('{*}url/{*}loc').text,
                         self.get_url('/en/'))

    def test_one_page_en_it(self):
        from cms.utils.conf import get_languages
        page = self.create_page(language='en')
        title = create_title('it', 'ciao', page)
        # unpublished
        elem = self.get_sitemap()
        self.assertEqual(len(list(elem)), 1)
        # publish title
        publish_page(page, self.get_superuser())
        elem = self.get_sitemap()
        self.assertEqual(len(list(elem)), 2)
        self.assertEqual([self.get_url('/en/'), self.get_url('/it/')],
                         [e.text for e in elem.findall('{*}url/{*}loc')])
        links = [e.attrib for e in elem.find('{*}url').findall('{*}link')]
        self.assertEquals(
            links,
            [{'rel': 'alternate', 'hreflang': lang,
              'href': self.get_url(url)}
             for lang, url in (('en', '/en/'), ('it', '/it/'))])
