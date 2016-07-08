from setuptools import setup

setup(
    name="paradrop",
    version="0.3.0",
    author="Paradrop Labs",
    description="Paradrop wireless virtualization",
    install_requires=[
        'docker-py',
        'ipaddress',
        'twisted',
        'txdbus',
        'wget',
        'pyyaml',
        'pdtools',
        'mock',
        'flask',
        'smokesignal',
        'bcrypt>=2.0.0',
        'cffi>=1.1.2',
        'colorama>=0.3.3',
        'docopt>=0.6.2',
        'pyyaml>=3.11',
        'requests>=2.7.0',
        'service-identity>=14.0.0',
        'twisted==14.0.2',
        'enum34',
        'smokesignal>=0.7.0',
        'autobahn==0.10.5-2'
    ],

    packages=['paradrop'],
)
