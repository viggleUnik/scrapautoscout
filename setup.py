from setuptools import setup
from io import open

VERSION = '1.2.0'
DESCRIPTION = 'autoscout24 web scrapper'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="scrapautoscout",
    version=VERSION,
    author='Vicol Cristian',
    author_email='vicol.cristianken@gmail.com',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/viggleUnik/scrapautoscout',
    license='MIT',
    packages=['scrapautoscout'],
    install_requires=[
        'requests==2.28.2',
        'beautifulsoup4==4.11.1',
        'psycopg2-binary==2.9.5',
        'boto3==1.26.86',
        's3fs',
        'tqdm',
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={'console_scripts': ['scrapautoscout = scrapautoscout.pipeline:run']},
)
