#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    'py36-django19': [
        "pytest==5.4.1",
        "pytest-xdist",
        "tox==3.14.6",
    ],
    'flake8': [
        "flake8==3.7.9",
        "isort>=4.2.15,<5",
        "mypy==0.770",
        "pydocstyle>=3.0.0,<4",
    ]
}

extras_require['dev'] = (
    extras_require['dev'] +  # noqa: W504
    extras_require['py36-django19'] +  # noqa: W504
    extras_require['flake8']
)


with open('./README.md') as readme:
    long_description = readme.read()


setup(
    name='4byte-directory',
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version='0.1.0-alpha.0',
    description="""4byte-directory: Registry of 4byte function, event signatures and \
        their human readable counterparts.""",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Piper Merriam',
    author_email='piper@pipermerriam.com',
    url='https://github.com/pipermerriam/ethereum-function-signature-registry',
    include_package_data=True,
    install_requires=[
        "eth-utils>=1,<2",
    ],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    py_modules=[''],
    license="MIT",
    zip_safe=False,
    keywords='ethereum',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
)
