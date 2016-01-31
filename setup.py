import sys

from setuptools import find_packages, setup

install_requires = [
    'influxdb>=2.11.0',
    'click>=5.1',
    'terminaltables>=2.1.0',
    'six>=1.10.0'
]

if sys.version_info < (3, 4, ):
    install_requires.append('trollius>=2.0')


setup(
    name='tourbillon',
    version='0.6',
    description='A Python agent for collecting metrics and store them into'
    ' an InfluxDB.',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'tourbillon = tourbillon.agent.cli:main'
        ]
    },
    zip_safe=False,
    namespace_packages=['tourbillon'],
    author='The Tourbillon Team',
    author_email='tourbillonpy@gmail.com',
    url='https://github.com/tourbillonpy/tourbillon-agent',
    license='ASF',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Monitoring',
    ],
    keywords='monitoring metrics agent influxdb',
)
