from setuptools import setup, find_packages


setup(
    name = 'doyoumind',
    version = '1.0.0',
    author = 'Ohad Avnery',
    description = 'A mind parser, how cool!',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)