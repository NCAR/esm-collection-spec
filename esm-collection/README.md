# ESM Collection Specification

- **Title: ESM Collection**
- **Identifier: esm**
- **Field Name Prefix: esm**
- **Scope: Collection**
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/blob/master/extensions/README.md#extension-maturity): Proposal**

This document explains the fields of the Earth System Model (ESM) extension which extends the [STAC Collection](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md).

The Earth System Model STAC extension describes a way of cataloging large datasets with a homogeneous metadata structure, such as those produced by the [Coupled Model Intercomparison Project (CMIP)](https://www.wcrp-climate.org/wgcm-cmip) of the World Climate Research Programme.

- [Example](./examples/sample-pangeo-cmip6-collection.json)
- [JSON Schema](./json-schema/schema.json)

## Collection Fields

This extension introduces two new fields at the top level of the collection: `esm:attributes` and `esm:aggregation_control`.

| Field Name              | Type                                                          | Description                                                                                 |
| ----------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| assets                  | Map<string, [ESM Asset Object](#esm-asset-object)>            | **REQUIRED.** A dictionary of assets.                                                       |
| esm:attributes          | [string]                                                      | **REQUIRED.** A list of attributes (columns) in the catalog flat table.                     |
| esm:aggregation_control | [Aggregation Control Object](#esm-aggregation-control-object) | Description of how to support aggregation of multiple assets into a single xarray data set. |

## ESM Asset Object

An asset is an object that contains a link to data associated with the Item that can be downloaded
or streamed. It is allowed to add additional fields.

| Field Name       | Type      | Description                                                                                                                                                                                  |
| ---------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| href             | string    | **REQUIRED.** Link to the asset object. Relative and absolute links are both allowed.                                                                                                        |
| title            | string    | The displayed title for clients and users.                                                                                                                                                   |
| description      | string    | A description of the Asset providing additional details, such as how it was processed or created. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| type             | string    | [Media type](#media-types) of the asset.                                                                                                                                                     |
| roles            | \[string] | The [semantic roles](#asset-role-types) of the asset, similar to the use of `rel` in links.                                                                                                  |
| esm:data_field   | string    | **REQUIRED**. The name of the column containing the path to the asset.                                                                                                                       |
| esm:format       | string    | The file or data format of the assets. Valid are `netcdf` and `zarr`. If specified, it means that all data in the catalog are the same type.                                                 |
| esm:format_field | string    | The column name which contains the data format, allowing for heterogeneous data formats in one catalog. Mutually exclusive with `esm:format`.                                                |
| esm:row          |           |                                                                                                                                                                                              |

Beyond to the fields above, any of the [additional fields](#additional-fields) _may_ be added to the assets. But this
is recommended only in special cases, see [Additional Fields for Assets](#additional-fields-for-assets)) for more information.

### Asset Role Types

Like the Link `rel` field, the `roles` field can be given any value, however here are a few standardized role names.

| Role Name      | Description                                               |
| -------------- | --------------------------------------------------------- |
| esm-catalog    | mime-type, what the role should link to (csv), what fiels |
| esm-vocabulary |                                                           |
| esm-asset      |                                                           |

## ESM Aggregation Control Object

An aggregation control object defines necessary information to use when aggregating multiple assets into a single xarray dataset.

| Field Name     | Type                                        | Description                                                                                                                                                |
| -------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| variable_field | string                                      | **REQUIRED**. Name of the attribute column in csv file that contains the variable name.                                                                    |
| groupby_attrs  | array                                       | Column names (attributes) that define data sets that can be aggregated.                                                                                    |
| aggregations   | [[Aggregation Object](#aggregation-object)] | List of aggregations describing types of operations done during the aggregation (concatenation & merging) of multiple assets into a single xarray dataset. |

## Aggregation Object

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
