import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.txt")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read()

requires = [
    "ago",
    "alembic",
    "appdirs",
    "arrow",
    "Babel",
    "beautifulsoup4",
    "black",
    "bs4",
    "certifi",
    "chardet",
    "click",
    "FormEncode",
    "gevent",
    "greenlet",
    "gunicorn",
    "hupper",
    "idna",
    "Jinja2",
    "linecache2",
    "lingua",
    "lxml",
    "Mako",
    "MarkupSafe",
    "mypy-extensions",
    "mysql-connector-python",
    "nose",
    "PasteDeploy",
    "pathspec",
    "plaster",
    "plaster-pastedeploy",
    "polib",
    "protobuf",
    "Pygments",
    "PyJWT",
    "pyramid",
    "pyramid-debugtoolbar",
    "pyramid-jinja2",
    "pyramid-mako",
    "pyramid-retry",
    "pyramid-tm",
    "python-dateutil",
    "python-editor",
    "pytz",
    "PyUtilib",
    "pyxform",
    "regex",
    "repoze.lru",
    "requests",
    "six",
    "soupsieve",
    "SQLAlchemy",
    "toml",
    "traceback2",
    "transaction",
    "translationstring",
    "twilio",
    "typed-ast",
    "typing-extensions",
    "unicodecsv",
    "unittest2",
    "urllib3",
    "venusian",
    "waitress",
    "WebHelpers2",
    "WebOb",
    "xlrd",
    "zope.deprecation",
    "zope.event",
    "zope.interface",
    "zope.sqlalchemy",
    "validators",
    "cryptography",
]

tests_require = [
    "WebTest >= 1.3.1",  # py3 compat
    "pytest",
    "pytest-cov",
]

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
    extras_require={
        "testing": tests_require,
    },
    install_requires=requires,
    entry_points={
        "paste.app_factory": [
            "main = ushauri:main",
        ],
        "console_scripts": [
            "create_superuser = ushauri.scripts.createsuperuser:main",
            "configure_alembic = ushauri.scripts.configurealembic:main",
        ],
    },
)
