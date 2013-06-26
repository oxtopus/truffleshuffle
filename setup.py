from setuptools import setup

version = {}
execfile('truffleshuffle/__version__.py', {}, version)

requirements = map(str.strip, open('requirements.txt').readlines())

setup(
  name = 'truffleshuffle',
  version = version['__version__'],
  description = "S3 Multipart Upload Utility",
  classifiers = \
    [
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Topic :: Software Development :: Libraries',
    ],
  keywords = 's3',
  author = 'Austin Marshall',
  author_email = 'oxtopus@gmail.com',
  url = 'https://github.com/oxtopus/truffleshuffle',
  license = 'MIT',
  namespace_packages = ['truffleshuffle'],
  package_dir = \
    {
      'truffleshuffle': 'truffleshuffle'
    },
  packages = ['truffleshuffle'],
  entry_points = \
    {
      'console_scripts': \
        [
          'upload-s3-multipart = truffleshuffle.upload:main'
        ]
    },
  requires = requirements,
  install_requires = requirements
)