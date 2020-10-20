#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import seshkit as seshkit_project_vals

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'boto3>=1.15',
    'Click>=7.0',
    'colorama',
    'jinja',
    'requests',
 ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    version=seshkit_project_vals.__version__,
    author=seshkit_project_vals.__author__,
    author_email=seshkit_project_vals.__email__,
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="seshkit is a command-line tool for creating transcripts from audio files.",
    entry_points={
        'console_scripts': [
            'sesh=seshkit.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='seshkit',
    name='seshkit',
    packages=find_packages(include=['seshkit', 'seshkit.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dannguyen/seshkit',
    zip_safe=False,
)
