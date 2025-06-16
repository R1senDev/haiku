from setuptools import setup, find_packages


setup(
    name                          = 'haiku',
    version                       = '0.1.0',
    author                        = 'R1senDev',
    author_email                  = 'ris3nanderson@gmail.com',
    description                   = 'Simple Haiku manager',
    long_description              = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/R1senDev/haiku.git',
    packages                      = find_packages(),
    classifiers                   = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires               = '>=3.6'
)
