import os
import sys

from setuptools import find_packages, setup

version = __import__('yearn').__version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


required_pkgs = [
    'pydantic>=1',
    'torrentool>=1',
    'humanfriendly>=9',
    'click>=8',
]

classifiers = [
    "Development Status :: 3 - Alpha"
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Communications :: File Sharing",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name="yearn-client",
    version=version,
    url='https://github.com/jonesnc/yearn-client',
    author='Nathan Jones',
    author_email='nathanjones930@gmail.com',
    maintainer='Nathan Jones',
    maintainer_email='nathanjones930@gmail.com',
    description='YEt Another RtorreNt client',
    long_description=read("README.md"),
    keywords="yearn rtorrent api bittorrent",
    license="MIT",
    packages=find_packages(),
    scripts=[],
    install_requires=required_pkgs,
    classifiers=classifiers,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'yearn = yearn.scripts.yearn:cli'
        ]
    }
)
