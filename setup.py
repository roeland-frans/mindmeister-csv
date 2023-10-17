from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="mm2csv",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["mm2csv = mm2csv:main"]},
    install_requires=[],
)
