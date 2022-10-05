from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pyneato",
    version="0.0.1",
    description="Python package for controlling Neato pyneato Connected vacuum robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Benjamin Paap",
    author_email="benjamin.paap@gmail.com",
    url="https://github.com/benjaminpaap/pyneato",
    license="Licensed under the MIT license. See LICENSE file for details",
    packages=["pyneato"],
    package_dir={"pyneato": "pyneato"},
    package_data={"pyneato": ["cert/*.crt"]},
    install_requires=["requests", "requests_oauthlib", "voluptuous"],
)
