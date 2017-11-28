from distutils.core import setup

setup(
  name = 'genword',
  packages = ['genword', 'genword.lib'], # this must be the same as the name above
  version = '0.1',
  description = 'A framework to manipulate Word files',
  author = 'Diego Fernandez',
  author_email = 'di3g0bs0n@gmail.com',
  url = 'https://github.com/di3g0bs0n/genword', # use the URL to the github repo
  keywords = ['framework', 'word', 'office', 'document'], # arbitrary keywords
  classifiers = [],
  package_data = {'genword': ['data/empty.dat']},
  include_package_data=True

)