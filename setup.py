from setuptools import setup, find_packages

setup(name='semaeval',
	  version='0.1',
	  description='Test and evaluate semantic engines.',
	  url='https://as-stash.axelspringer.de/scm/ideas/semaeval.git',
	  author='amaier1',
	  author_email='andreas.maier@asideas.de',
	  license='MIT',
	  packages=find_packages(),
	  install_requires=[
		  'requests',
		  'pyaml',
		  'python-dateutil',
		  'feedparser',
		  'semantria_sdk',
		  'textrazor',
		  'nltk',
		  'matplotlib',
		  'boilerpipe'
		  ],
	  include_package_data=True,
	  zip_safe=False)