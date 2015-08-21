from setuptools import setup, find_packages


setup(
    name='tourbillon',
    version='0.1',
    packages=find_packages(),
    install_requires=['influxdb==2.8.0', 'click==5.1'],
    entry_points={
        'console_scripts': [
            'tourbillon = tourbillon.agent.cli:main'
        ]
    },
    zip_safe=False,
    namespace_packages=['tourbillon']
)
