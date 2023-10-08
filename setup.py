from setuptools import setup, find_packages

setup(
    name='Wikipedia_Space_Scraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'bs4',
        'requests',
        'deep_translator',
        'tqdm'
    ]
)
