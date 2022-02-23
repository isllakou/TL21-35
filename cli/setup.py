from setuptools import setup
setup(
    name = 'cli',
    version = '0.1.0',
    packages = ['se2135'],
    install_requires=[
    'click',
    'requests'
    ],
    entry_points = {
        'console_scripts': [
            'se2135 = se2135.__main__:main'
        ]
    }
)
