from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'SQLAlchemy',
    'pymssql',
    'waitress',
    'bravado-core'
]

setup(
    name='jiva_fhir_api',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = apis:main'
        ],
    },
)