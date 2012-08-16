from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='magiccardsinfo',
      version=version,
      description="Set of classes for scarping MTG cards from magiccards.info",
      long_description="",
      classifiers=[],
      keywords='',
      author='Jeffrey Ness',
      author_email='flip387@gmail.com',
      url='',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['BeautifulSoup', 'unidecode'],
      test_suite='nose.collector',
      )
