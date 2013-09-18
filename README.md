# SEO utilities for Django CMS

A small collection of SEO utilities for Django CMS.

Delivers i18n-friendly sitemaps and `alternate` links.

Still in beta, be patient please.


## Install

	pip install git+https://github.com/mpaolini/django-cms-seoutils@master

There are no official releases yet.


## Configuration

Add `cms_seoutils` to `INSTALLED_APPS` *before* `django.contrib.sitemaps`

Django settings:
- `CMS_SEOUTILS_REDIRECTORS` (default `False`) enables/disables
  listing of `x-default` alternatives.


## Internationalized sitemaps

An i18n aware drop-in replacement for `cms.sitemaps.cms_sitemaps.CMSSitemap`
with support for `rel="alternate"` and `hreflang` attributes.

See https://support.google.com/webmasters/answer/2620865?hl=en&ref_topic=2370587
for more info.

	from cms_seoutils.sitemaps import CMSI18nSitemaps
	urlpatterns = (
		'',
        # stuff here
        url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSI18nSitemap}})


## rel="alternate" links

Generates alternate language links like:
`<link rel="alternate" hreflang="de" href="http://www.example.com/de">` and
`<link rel="alternate" hreflang="x-default" href="http://www.example.com/de">`.

See https://support.google.com/webmasters/answer/189077?hl=en&ref_topic=2370587
for more info.

To use it, add

	{% use "cms_seoutils" %}
	
to your base template (or where appropriate).

Then in the `<head>` section add

	{% cms_seoutils_alternate %}


## Testing

Install all packages listed in requirements/dev.txt and run `test.py`:

    pip install -r requirements/dev.txt
	python test.py


## Notes

Make sure you use `i18n_patterns` in your `urls.py` when including DjangoCMS
urls (without it DjangoCMS won't work properly anyways).

Has nothing to do with this software, but remember some crawlers can use
`robots.txt` to locate a sitemap.


## TODO

Find out a bit more on (`lang="x-default"`) links and enable them by default.

0.1 release

Automated tests against differend django and django-cms versions.

Travis-CI.


test with different settings combinations:

    {'USE_I18N': False}
    {'CMS_LANGUAGES': {'default': {'HIDE_UNTRASLATED': False}}}
    {'CMS_LANGUAGES': {'default': {'PUBLIC': False}}}
    {'CMS_LANGUAGES': {'default': {'REDIRECT_ON_FALLBACK': False}}}

    CMS_SEOUTILS_REDIRECTORS = False
