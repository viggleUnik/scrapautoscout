from setuptools import setup
from io import open

VERSION = '0.0.1'
DESCRIPTION = 'autoscout24 web scrapper'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(

    name="scrapautoscout",
    version=VERSION,

    author='viggleUnik',
    author_email='vicol.cristianken@gmail.com',

    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/viggleUnik/scrapautoscout',

    license='MIT',

    packages=['scrapautoscout'],
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
    entrypoints={
        'console_scripts' : ['scrapautoscout=scrapautoscout.main:main']
    }
)
