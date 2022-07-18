from importlib.metadata import entry_points
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="oar-filemanager",
    python_requires=">=3.6",
    version="1.0.0",
    description="OAR Filemanager Service API.",
    author="Omar I. EL MIMOUNI",
    author_email="omarilias.elmimouni@nist.gov",
    url="https://github.com/usnistgov/oar-filemanager-api",
    packages=find_packages(include=["nistoar", "nistoar.*"], exclude=["tests"]),
    install_requires=required,
    setup_requires=["pytest-runner", "flake8"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["oarfm=nistoar.filemanager.main:main"]},
    package_data={"nistoar.filemanager": ["data/*"]},
)
