from setuptools import setup, find_packages
from setuptools.command.install import install as default_install


class Install(default_install):
	def run(self):
		default_install.do_egg_install(self)
		import nltk
		nltk.download("all")

setup(name='semaeval',
	  version='0.1.3',
	  description='Test and evaluate semantic engines.',
	  url='https://as-stash.axelspringer.de/scm/ideas/semaeval.git',
	  author='amaier1',
	  author_email='andreas.maier@asideas.de',
	  cmdclass={'install': Install},
	  license='MIT',
	  packages=find_packages(),
	  setup_requires=['nltk'],
	  install_requires=[
		  'boilerpipe',
		  'nltk',
		  'requests',
		  'pyaml',
		  'python-dateutil',
		  'feedparser',
		  'semantria_sdk',
		  'textrazor',
		  ],
	  include_package_data=True,
	  zip_safe=False)