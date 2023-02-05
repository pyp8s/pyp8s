import setuptools
from version import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-p8s-metrics",
    version=version,
    author="Pavel Kim",
    author_email="hello@pavelkim.com",
    description="Customisable prometheus exporter for your python application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reinvented-stuff/py-p8s-metrics",
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
