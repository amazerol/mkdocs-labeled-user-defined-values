from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mkdocs-labeled-user-defined-values",
    version="1.0.5",
    description="An enhanced version of mkdocs-user-defined-values. Keywords can now be categorized.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amazerol/mkdocs-labeled-user-defined-values",
    author="Alban MAZEROLLES",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="mkdocs plugin multiple user defined value",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3, <4",
    install_requires=["mkdocs==1.*"],
    extras_require={"dev": ["pipenv-setup", "pylint", "black", "pytest",]},
    dependency_links=[],
    entry_points={
        "mkdocs.plugins": ["labeled-user-defined-values = mkdocs_labeled_user_defined_values.plugin:LabeledUserDefinedValues",]
    },
    project_urls={
        "Bug Reports": "https://github.com/amazerol/mkdocs-labeled-user-defined-values/issues",
        "Source": "https://github.com/amazerol/mkdocs-labeled-user-defined-values/",
    },
)
