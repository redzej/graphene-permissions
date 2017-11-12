from setuptools import setup

setup(
    name='graphene-permissions',
    packages=['graphene_permissions'],
    license='MIT',
    version='0.1.1',
    author='redzej',
    description='Simple graphene-django permission system',
    url='https://github.com/redzej/graphene-permissions',
    download_url='https://github.com/redzej/graphene-permissions/archive/0.1.tar.gz',
    keywords=['graphene', 'django', 'permissions'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
    ],
)
