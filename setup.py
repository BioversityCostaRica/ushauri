import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.txt")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read()

requires = [
    "plaster_pastedeploy",
    "pyramid >= 1.9a",
    "pyramid_debugtoolbar",
    "pyramid_jinja2",
    "pyramid_retry",
    "pyramid_tm",
    "SQLAlchemy",
    "transaction",
    "zope.sqlalchemy",
    "waitress",
    "webhelpers2",
    "ago",
    "arrow",
    "PyCrypto",
    "pyutilib == 5.4.1",
    "formencode",
    "Babel",
    "lingua",
    "lxml",
    "mysql-connector-python",
    "bs4",
    "alembic",
    "gunicorn",
    "gevent",
    "twilio",
]

tests_require = ["WebTest >= 1.3.1", "pytest", "pytest-cov"]  # py3 compat

setup(
    name="ushauri",
    version="0.0",
    description="Ushauri-Agricultural Advice Service",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="",
    author_email="",
    url="",
    keywords="web pyramid pylons",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={"testing": tests_require},
    install_requires=requires,
    entry_points={
        "paste.app_factory": ["main = ushauri:main"],
        "console_scripts": [
            "initialize_ushauri_db = ushauri.scripts.initializedb:main"
        ],
    },
)
