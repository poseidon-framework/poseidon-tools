# poseidonPy
Python API for working with Poseidon databases

# Internal dev notes

## Recommended pipeline
- Install miniconda
- Create new environment for this package, for example `conda create --name poseidon-dev python`.
- To install the package for local testing: `pip install -e .` You can then fire up the python interpreter via `python` and load the module via `import poseidon-tools`.
- To run the tests, run `pytest`.

Overview of python package development: [https://python-packaging.readthedocs.io/en/latest/index.html](https://python-packaging.readthedocs.io/en/latest/index.html)

To test and develop yourself, I recommend using virtual environments (e.g. via `conda` or `python -m venv`) and then `pip install . -e`, which installs the package and runs the tests into your active environment, and creates symlinks instead of copies of files, such that changes in your repo will immediately be available.


