# ESM Collection Schema Validation

- [ESM Collection Schema Validation](#esm-collection-schema-validation)
  - [Python Validator](#python-validator)
    - [Installation](#installation)
    - [Usage](#usage)

This directory includes installation instructions for a Python validator for the esm-collection-spec.

## Python Validator

### Installation

The validator can be installed in any of the following ways:

Using Pip via PyPI:

```bash
python -m pip install esmcol-validator
```

Using Conda:

```bash
conda install -c conda-forge esmcol-validator
```

Or from the source repository:

```bash
python -m pip install git+https://github.com/NCAR/esmcol-validator.git
```

### Usage

```bash
$ esmcol-validator --help
Usage: esmcol-validator [OPTIONS] ESMCOL_FILE

  A utility that allows users to validate esm-collection json files against
  the esm-collection-spec.

Options:
  --esmcol-spec-dirs TEXT
  --version TEXT           [default: master]
  --verbose                [default: False]
  --timer                  [default: False]
  --log-level TEXT         [default: CRITICAL]
  --help                   Show this message and exit.
```

Example:

```bash
$ esmcol-validator sample-pangeo-cmip6-collection.json
{'collections': {'valid': 1, 'invalid': 0}, 'catalog_files': {'valid': 1, 'invalid': 0}, 'unknown': 0}
{
    "collections": {
        "valid": 1,
        "invalid": 0
    },
    "catalog_files": {
        "valid": 1,
        "invalid": 0
    },
    "unknown": 0
}
```
