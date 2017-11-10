import bot_chucky
from setuptools import setup

VERSION = bot_chucky.__version__
AUTHOR = bot_chucky.__author__

setup_kwargs = {
    'name': 'bot_chucky',
    'version': VERSION,
    'url': 'https://github.com/MichaelYusko/Bot-Chucky',
    'license': 'MIT',
    'author': AUTHOR,
    'author_email': 'freshjelly12@yahoo.com',
    'description': 'Python bot which able to work with messenger of facebook',
    'packages': ['bot_chucky'],
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License'
    ],
 }

requirements = [
    'requests==2.17.3',
    'facebook-sdk==2.0.0',
    'soundcloud==0.5.0',
    'python-twitter==3.3',
    'bs4==0.0.1'
]

setup_kwargs['install_requires'] = requirements

setup(**setup_kwargs)

print(u"\n\n\t\t    "
      "BotChucky version {} installation succeeded.\n".format(VERSION))
