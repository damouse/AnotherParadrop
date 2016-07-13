from setuptools import setup, find_packages

setup(
    name="paradrop",
    version="0.3.0",
    author="Paradrop Labs",
    description="Paradrop wireless virtualization",
    install_requires=[
        'docker-py',
        'ipaddress',
        'txdbus',
        'pyyaml',
        'smokesignal',
        'colorama>=0.3.3',
        'docopt>=0.6.2',
        'pyyaml>=3.11',
        'requests>=2.7.0',
        'service-identity>=14.0.0',
        'twisted>=14.2',
        'smokesignal>=0.7.0',
        'autobahn==0.10.5-2'
    ],

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'paradrop=paradrop:main',
            'pdconfd=paradrop:run_pdconfd'
        ],
    },
)
