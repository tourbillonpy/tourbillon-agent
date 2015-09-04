import sys

from setuptools import find_packages, setup

PY34_PLUS = sys.version_info[0] == 3 and sys.version_info[1] >= 4

exclude = ['tourbillon.agent.agent2'
           if PY34_PLUS else 'tourbillon.agent.agent']

install_requires = ['influxdb>=2.8.0', 'click==5.1']

if not PY34_PLUS:
    install_requires.append('trollius==2.0')


setup(
    name='tourbillon',
    version='0.2',
    packages=find_packages(exclude=exclude),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'tourbillon = tourbillon.agent.cli:main'
        ]
    },
    zip_safe=False,
    namespace_packages=['tourbillon']
)
