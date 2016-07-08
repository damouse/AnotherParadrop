from setuptools import setup, find_packages

setup(
    name="paradrop",
    version="0.1.0",
    author="Paradrop Labs",
    description="Paradrop wireless virtualization",
    install_requires=[
        'flask'
    ],

    # package_dir={'': 'paradrop'},
    packages=find_packages(),
)
