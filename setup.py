from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

__author__ = "Denis Mulyalin <d.mulyalin@gmail.com>"

setup(
    name="py-ttr",
    version="0.3.2",
    author="Denis Mulyalin",
    author_email="d.mulyalin@gmail.com",
    description="Template Text Renderer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/dmulyalin/ttr",
    packages=find_packages(),
    package_data={
        "ttr": [
            "templates/*.txt",
            "templates/*/*.txt",
            "templates/*/*/*.txt",
            "templates/*/*/*/*.txt"
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
    python_requires=">=3.6",
    install_requires=[
        "PyYAML>=5.3.1",
        "openpyxl>=3.0.4",
        "Jinja2>=2.11.2"
    ],
    entry_points = {
        'console_scripts': ['ttr=ttr:cli_tool'],
    }
)
