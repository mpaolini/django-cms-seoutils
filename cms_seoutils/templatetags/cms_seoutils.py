from __future__ import absolute_import

from django import template

from cms.utils.i18n import get_current_language

from ..i18n import get_alternate


register = template.Library()


@register.inclusion_tag('cms_seoutils/alternate.html', takes_context=True)
def cms_seoutils_alternate(context):
    page = context.get('current_page')
    if page is not None:
        current_language = get_current_language()
        return {'alternate': [v for k, v in get_alternate(page).items()
                              if k != current_language]}
