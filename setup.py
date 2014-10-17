import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    ]

setup(name='Silently',
      version='0.1',
      description='Flask skeleton.',
      long_description=README,
      package_data = {'silently': ['templates/*.html',
                                   'templates/*.xml' ]},
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Mattias Granlund',
      author_email='mtsgrd@gmail.com',
      url='',
      packages=find_packages(exclude=("tests",)),
      keywords='',
      zip_safe=False,
      install_requires=requires,
      )
