# ESM Collection Specification

This document explains the structure and content of an ESM Collection.
A collection provides metadata about the catalog, telling us what we expect to find inside and how to open it.
The collection is described is a single json file, inspired by the STAC spec.

## Catalog fields

| Element      | Type          | Description                                                  |
| ------------ | ------------- | ------------------------------------------------------------ |
| esmcat_version | string      | **REQUIRED.** The ESM Catalog version the collection implements. |
| id           | string        | **REQUIRED.** Identifier for the collection.                    |
| title        | string        | A short descriptive one-line title for the collection.          |
| description  | string        | **REQUIRED.** Detailed multi-line description to fully explain the collection. [CommonMark 0.28](http://commonmark.org/) syntax MAY be used for rich text representation. |
| catalog_file | string | **REQUIRED.** Path to a the CSV file with the catalog contents. |
| attributes | [[Attribute Object](#attribute-object)] | **REQUIRED.** A list of attribute columns in the dataset. |
| assets | [Asset Object](#assets-object) | **REQUIRED**. Description o how the assets (data files) are referenced in the CSV catalog file.

### Attribute Object

An attribute object describes a column in the catalog CSV file.
The column names can optionally be associated with a controlled vocabulary, such as the [CMIP6 CVs](https://github.com/WCRP-CMIP/CMIP6_CVs), which explain how to interpret the attribute values.

| Element | Type | Description |
| ------- | ---- | ------------|
| column_name | string | **REQUIRED.** The name of the attribute column. Must be in the header of the CSV file. |
| vocabulary | string | Link to the controlled vocabulary for the attribute in the format of a URL. |

### Assets Object

An assets object describes the columns in the CSV file relevant for opening the actual data files.

| Element | Type | Description |
| ------- | ---- | ------------|
| column_name | string | **REQUIRED.** The name of the column containing the path to the asset. Must be in the header of the CSV file. |
| format | string | The data format. Valid values are `netcdf` and `zarr`. If specified, it means that all data in the catalog is the same type. |
| format_column_name | string | The column name which contains the data format, allowing for variable data types in one catalog. Mutually exclusive with `format`. |
