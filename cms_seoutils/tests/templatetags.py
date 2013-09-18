from lxml import etree

from cms.api import create_page, create_title, publish_page, add_plugin

from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.test.utils import override_settings
from django.utils.translation import override

from cms_seoutils.tests.utils import get_cms_languages, SEOUtilsTestCase


class TemplatetagsTestCase(SEOUtilsTestCase):

    def get_page(self, page, language, **opts):
        with override(language):
            resp = self.client.get(page.get_absolute_url(), **opts)
        self.assertEqual(resp.status_code, 200)
        return etree.fromstring(resp.content)

    def test_empty(self):
        page = self.create_page(language='en', template='page.html')
        elem = self.get_page(page, 'en')
        links = [e.attrib for e in elem.findall('head/link')]
        self.assertEquals([], links)

    @override_settings(CMS_LANGUAGES=get_cms_languages(
            {1: [{'code': 'it', 'hide_untranslated': False}]}))
    def test_one_page_en_show_untranslated(self):
        page = self.create_page(language='en', template='page.html')
        elem = self.get_page(page, 'en')
        links = [e.attrib for e in elem.findall('head/link')]
        self.assertEqual(
            links,
            [{'href': 'http://example.com/it/', 'rel': 'alternate',
              'hreflang': 'it'}])

    def test_one_page_en_it(self):
        page = self.create_page(language='en', template='page.html')
        title = create_title('it', 'ciao', page)
        # unpublished
        elem = self.get_page(page, 'en')
        links = [e.attrib for e in elem.findall('head/link')]
        self.assertEqual(links, [])
        # publish title
        publish_page(page, self.get_superuser())
        # get en
        elem = self.get_page(page, 'en')
        links = [e.attrib for e in elem.findall('head/link')]
        self.assertEqual(
            links,
            [{'href': 'http://example.com/it/', 'rel': 'alternate',
              'hreflang': 'it'}])
        # get it
        elem = self.get_page(page, 'it')
        links = [e.attrib for e in elem.findall('head/link')]
        self.assertEqual(
            links,
            [{'href': 'http://example.com/en/', 'rel': 'alternate',
              'hreflang': 'en'}])
