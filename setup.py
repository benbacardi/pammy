'''Setup file for pammy'''
from setuptools import setup, find_packages
from pammy.version import __VERSION__

import sys

INSTALL_REQUIRES = [
    'django',
    'django_autoconfig',
    'netaddr',
]

setup(
    name=-'pammy',
    version=__VERSION__,
    packages=find_packages(),
    description='IP Address Management tool',
    long_description=open('README.rst').read(),
    author='Ben Cardy',
    author_email='benbacardi@gmail.com',
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    test_suite           = 'setuptest.setuptest.SetupTestSuite',
    tests_require        = ['django-setuptest>=0.1.5'],
    url='https://github.com/benbacardi/pammy',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)
