# ESM Collection Specification

- **Title: ESM Collection**
- **Identifier: esm**
- **Field Name Prefix: esm**
- **Scope: Collection**
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/blob/master/extensions/README.md#extension-maturity): Proposal**

This document explains the fields of the STAC Earth System Model (ESM) Extension to a STAC Collection.
ESM data is considered to be data produced by simulations models of the earth for a data specific model domain and temporal extent.

- [Example](./examples/sample-pangeo-cmip6-collection.json)
- [JSON Schema](./json-schema/schema.json)

## Collection Fields

This extension introduces a three new fields at the top level of the collection: `esm:catalog`, `esm:attributes` and `esm:aggregation_control`.

| Field Name              | Type                                                          | Description                                                                                               |
| ----------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| esm:catalog             | Map<string, [ESM Catalog Object](#esm-catalog-object)>        | A dictionary of assets. Required if `assets.catalog` not defined.                                         |
| esm:attributes          | [string]                                                      | **REQUIRED.** A list of attribute columns in the data set.                                                |
| esm:aggregation_control | [Aggregation Control Object](#esm-aggregation-control-object) | **OPTIONAL.** Description of how to support aggregation of multiple assets into a single xarray data set. |

### ESM Catalog Object

TODO. Pending spec.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
|            |      |

### ESM Aggregation Control Object

An aggregation control object defines necessary information to use when aggregating multiple assets into a single xarray dataset.

| Field Name     | Type                                      | Description                                                                                                                                                |
| -------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| variable_field | string                                    | **REQUIRED**. Name of the attribute column in csv file that contains the variable name.                                                                    |
| groupby_attrs  | array                                     | Column names (attributes) that define data sets that can be aggregated.                                                                                    |
| aggregations   | [Aggregation Object](#aggregation-object) | List of aggregations describing types of operations done during the aggregation (concatenation & merging) of multiple assets into a single xarray dataset. |

### Aggregation Object

| Field Name     | Type   | Description                                                                                                                                                                                                                                                                                                                                                                         |
| -------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| type           | string | **REQUIRED**. Type of aggregation operation to apply. Valid values are: `join_new` (concatenate a list of datasets along a new dimension), `join_existing` (concatenate a list of datasets along an existing dimension), `union` (merge a list of datasets into a single dataset)                                                                                                   |
| attribute_name | string | Name of attribute (column) along which to aggregate assets.                                                                                                                                                                                                                                                                                                                         |
| options        | object | Aggregration settings that are passed as keywords arguments to [xarray.concat()](https://xarray.pydata.org/en/stable/generated/xarray.concat.html) and [xarray.merge()](https://xarray.pydata.org/en/stable/generated/xarray.merge.html#xarray.merge). For `join_existing`, it must contain the name of the existing dimension to use (for e.g.: something like `{'dim': 'time'}`). |

## Implementations

ESM has multiple implementations. Some example collections:

- [CMIP6 collection in the Google Public Datasets Program]() (STAC v. pending)
- [CESM Large Ensemble Data in the AWS Public Datasets Program]() (STAC v. pending)

Additionally, [Intake-ESM](https://intake-esm.readthedocs.io/en/latest/) provides a Python toolkit for using ESM catalogs.
