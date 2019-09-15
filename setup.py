from setuptools import setup

setup(
    name = 'camulator',
    version = '0.1',
    author_email = 'daniel.czech@protonmail.com',
    packages = ['camulator'],
    entry_points = {
        'console_scripts': ['camulator = camulator.cli:cli']},
    install_requires = [],
) 
