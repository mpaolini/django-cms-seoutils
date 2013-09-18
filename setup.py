from setuptools import setup, find_packages

from cms_seoutils import get_version

with open('requirements/base.txt') as f:
    REQUIRES = f.read()

setup(
    name = "django-cms-seoutils",
    url = 'https://github.com/mpaolini/django-cms-seoutils',
    author = 'Marco Paolini',
    author_email = 'markopaolini@gmail.com',
    description = 'SEO utilities for DjangoCMS',
    version = get_version(),
    packages = find_packages(),
    include_package_data = True,
    install_requires = REQUIRES
)
