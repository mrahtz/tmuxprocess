from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tmuxprocess',
    version='0.2.0',
    description='Redirect I/O from processes to different tmux windows',
    long_description=long_description,
    url='https://github.com/mrahtz/tmuxprocess',
    author='Matthew Rahtz',
    author_email='matthew.rahtz@gmail.com',
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='multiprocessing process tmux',
    py_modules=["tmuxprocess"],
)
