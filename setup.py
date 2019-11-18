from setuptools import setup


setup(
    name='crawler',
    version='0.1.0',
    description='Crawling service',
    url='',
    author='Quvele',
    author_email='alina.baimasheva@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7.0',
    packages=['crawler'],
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'lxml',
        'patool',
    ],
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'crawl = crawler.runner:start_crawling',
        ],
    },
)
