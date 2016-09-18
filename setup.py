from setuptools import setup, find_packages


setup(
    name='Tornado API Builder',
    version='0.5',
    description='REST API Builder for Tornado',
    packages=find_packages(),
    author='Aleksandr Kaurdakov',
    install_requires=[
        'tornado',
    ],
)
