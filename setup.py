from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="poseidon-tools",
    version="0.0.1",
    author="Stephan Schiffels",
    author_email="schiffels@shh.mpg.de",
    description="A package to work with Poseidon Archaeogenetics modules",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/poseidon-framework/poseidon-tools",
    install_requires=[
          'csvw'
    ],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.7'
)