from graphene_permissions import __version__
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

install_requirements = parse_requirements('requirements/requirements.txt', session=PipSession())

setup(
    name='graphene-permissions',
    packages=('graphene_permissions',),
    license='MIT',
    version=__version__,
    author='redzej',
    description='Simple graphene-django permission system.',
    long_description=long_description,
    url='https://github.com/redzej/graphene-permissions',
    install_requires=[str(ir.req) for ir in install_requirements],
    keywords='graphene django permissions permission system',
    python_requires='>=3.5',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
    ),
)
