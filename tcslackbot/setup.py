""" package the app
    reference http://www.plankandwhittle.com/packaging-a-flask-web-app/ """

import os

from setuptools import setup, find_packages

setup(
    name='tcslackbot',
    version='0.1.0',
    description='Slack bot to watch for TeamCity links and grab more data from them.',
    long_description=('see README'),
    url='https://github.com/warnerpr/slack-teamcity-bot',
    license='MIT',
    author='Paul Warner',
    author_email='paul.warner@gmail.com',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Flask==0.10.1',
        'Jinja2==2.7.3',
        'MarkupSafe==0.23',
        'Werkzeug==0.10.1',
        'argparse==1.2.1',
        'itsdangerous==0.24',
        'requests==2.5.1',
        'wsgiref==0.1.2'],
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'dev_server = tcslackbot.scripts.run_server:dev_server',
            'run_server = tslackbot.scripts.run_server:run_server'
        ]
    },
    package_data={},
    classifiers=[],
)
