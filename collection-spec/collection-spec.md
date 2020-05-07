# ESM Collection Specification

- **Title: ESM Collection**
- **Identifier: esm**
- **Field Name Prefix: esm**
- **Scope: Collection**
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/blob/master/extensions/README.md#extension-maturity): Proposal**

This document explains the fields of the STAC Earth System Model (ESM) Extension to a STAC Collection.
ESM data is considered to be data produced by simulations models of the earth for a data specific model domain and temporal extent.

- [Example](examples/sample-pangeo-cmip6-collection.json)
- [JSON Schema](json-schema/schema.json)

### Collection Fields

This extension introduces a three new fields at the top level of the collection:  `esm:catalog`, `esm:attributes` and `esm:aggregation_control`.

| Field Name | Type                                       | Description |
| ---------- | ------------------------------------------ | ----------- |
| esm:catalog | Map<string, [ESM Catalog Object](#esm-catalog-object)> | A dictionary of assets. Required if `assets.catalog` not defined. |
| esm:attributes | [string] | **REQUIRED.** A list of attribute columns in the data set. |
| esm:aggregation_control | [Aggregation Object](#aggregation-object) |  **OPTIONAL.** Description of how to support aggregation of multiple assets into a single xarray data set. |

### ESM Catalog Object

TODO. Pending spec.

| Field Name | Type                                       | Description |
| ---------- | ------------------------------------------ | ----------- |
| | |

## Implementations

ESM has multiple implementations. Some example collections:

- [CMIP6 collection in the Google Public Datasets Program]() (STAC v. pending)
- [CESM Large Ensemble Data in the AWS Public Datasets Program]() (STAC v. pending)

Additionally, [Intake-ESM](https://intake-esm.readthedocs.io/en/latest/) provides a Python toolkit for using ESM catalogs.

## Python Validator

### Installation

The [Python validator for the esm-collection-spec](https://github.com/NCAR/esmcol-validator) can be installed in any of the following ways:

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
