'''
Run all tests for package.
'''

import os

from django.core.management import call_command


def main():
    # initialize environment for test django project
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cms_seoutils.test_utils.project.settings'
    # run django tests
    call_command('test', 'cms_seoutils')


if __name__ == '__main__':
    main()
