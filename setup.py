import pathlib
from setuptools import setup, find_namespace_packages
from dhis2.core import __version__

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="dhis2",
    version=__version__,
    description="Tool for working and integrating with dhis2 instances.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhis2/dhis2-python-cli",
    author="Morten Hansen",
    author_email="morten@dhis2.org",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    # package_dir={'': 'src'},
    packages=find_namespace_packages(where=".", include=["dhis2.*"]),
    python_requires=">=3.8, <4",  # we might want to adjust this, starting low for now
    include_package_data=True,
    install_requires=["pyyaml", "click", "requests", "pydantic", "fhir.resources"],
    extras_require={},
    entry_points={
        "console_scripts": [
            "dhis2=dhis2.__main__:main",
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/dhis2/dhis2-python-cli/issues",
        "Source": "https://github.com/dhis2/dhis2-python-cli",
    },
)
