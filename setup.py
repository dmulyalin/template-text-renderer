from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

__author__ = "Denis Mulyalin <d.mulyalin@gmail.com>"

setup(
    name="ttr",
    version="0.1.0",
    author="Denis Mulyalin",
    author_email="d.mulyalin@gmail.com",
    description="Extendable Bulk Configuration Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/dmulyalin/ttr",
    packages=find_packages(),
    package_data={
        "ttr": [
            "templates/*"
        ]
    },
    include_package_data=True,
    data_files=[('', ['LICENSE'])],
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['ttr=ttr:cli_tool'],
    }
)