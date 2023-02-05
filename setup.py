import setuptools
from pyp8s import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyp8s",
    version=__version__,
    author="Pavel Kim",
    author_email="hello@pavelkim.com",
    description="Customisable prometheus exporter for your python application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyp8s/pyp8s",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
    ]
)
