from setuptools import setup

from graphene_permissions import __version__

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="graphene-permissions",
    packages=["graphene_permissions"],
    license="MIT",
    version=__version__,
    author="redzej",
    description="Simple graphene-django permission system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/redzej/graphene-permissions",
    keywords="graphene django permissions permission system",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Environment :: Web Environment",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 3.0",
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers"
    ],
)
