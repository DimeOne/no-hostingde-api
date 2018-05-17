import codecs
import os
from setuptools import setup

version = '0.1.3'
def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    dirname = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(dirname, filename), 'r').read()

install_requirements = read("requirements.txt").split()
long_description = read('README.md')

setup(name='no-hostingde-api',
      version=version,
      description='Unofficial Client for Hosting.de API',
      url='https://github.com/DimeOne/hostingde-api',
      author='Dominic S.',
      license='MIT',
      packages=['hostingde', 'hostingde.api', 'hostingde.helpers'],
      platforms='any',
      install_requires=install_requirements,
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords='hosting.de api client development',
      python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
      classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3.6",
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])