# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import crawler

setup(name='Ouroboros',
      version=crawler.__version__,
      description='callbacks sender',
      author=crawler.__author__,
      author_email=crawler.__author_email__,
      packages=[
          'ouroboros',
      ],
      scripts=[
          'bin/ouroboros'
      ]
)
