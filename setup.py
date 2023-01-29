from setuptools import setup

VERSION = '0.0.1'

setup(
    name='global-call',  # package name
    version=VERSION,  # package version
    description='A simple serverless function transformer,\
     and a simple way to call function in other language.',  # package description
    packages=['gbcall'],
    # package_dir={"": "src"},
    zip_safe=False,
    author="bi1lqv",
    author_email="bi1lqy.y@gmail.com",
    license="MIT",
    install_requires=[
        "aiohttp",
    ],
    entry_points={
        'console_scripts': [
            'gbcall = src.cli:prompt'
        ]
    }
)
