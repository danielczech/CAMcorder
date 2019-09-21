from setuptools import setup

setup(
    name = 'camcorder',
    version = '0.1',
    author_email = 'daniel.czech@protonmail.com',
    packages = ['camcorder'],
    entry_points = {
        'console_scripts': ['camcorder = camcorder.cli:cli']},
    install_requires = [
                       #'numpy == 1.14.1',
                       #'redis == 2.10.6'
                       ],
) 
