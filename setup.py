from setuptools import setup, find_packages

setup(
    name="pmon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": ["pmon=src.pmon.cli:main"],
    },
)
