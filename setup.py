try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

install_requires = [
    'tweepy==1.8',
    'pyyaml',
]

long_description = open('README.md').read()

setup(
    name='ciciol',
    author='fox',
    author_email='fox91 at anche no',
    version='0.1',
    description=('Lightweight and extremely customizable notifier. '
                 ' Designed to work with Twitter and much more'),
    url='http://github.com/volpino/Ciciol',
    packages=find_packages(),
    zip_safe=True,
    license='BSD',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: End Users/Desktop',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    long_description=long_description,
    install_requires=install_requires,
    scripts=["scripts/ciciol"]
)
