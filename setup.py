from setuptools import setup

setup(
    name='flasql',
    packages=['flasql'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pymods==2.0.5',
        'sickle'
    ],
)