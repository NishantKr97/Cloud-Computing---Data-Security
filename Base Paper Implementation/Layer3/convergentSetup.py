import os
from setuptools import setup, find_packages


setup(
    name = "convergent",
    description = "Convergent encryption library, encrypts with AES 256 CTR using the SHA256d hash of the plain text as key.",
    long_description = open('README.md').read(),
    version = "0.2",

    install_requires = ['setuptools'],

    package_dir = {'': '.'},
    packages = find_packages(),
    test_suite = "tests",

    url = 'https://github.com/HITGmbH/py-convergent-encryption',
    license = open("LICENSE.txt").read(),
    author = 'Hinnerk Haardt, HIT Information-Control GmbH',
    author_email = 'haardt@information-control.de',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security :: Cryptography',
    ]
)