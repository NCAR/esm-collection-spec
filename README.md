
:warning: Archived Repository Notice

This repository has been archived and is no longer actively maintained. The code and information contained within this repository may be outdated and may no longer be relevant to current usage.

**Development of this project has moved to https://github.com/intake/intake-esm and the up-to-date spec resides [here](https://github.com/intake/intake-esm/blob/main/docs/source/reference/esm-catalog-spec.md). Please check the https://github.com/intake/intake-esm repository for the latest updates and actively maintained specification.**



# ESM Catalog Specification

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/NCAR/esm-collection-spec/CI?label=CI&logo=github&style=for-the-badge)](https://github.com/NCAR/esm-collection-spec/actions?query=workflow%3ACI)
[![Zenodo](https://img.shields.io/badge/DOI-10.5281%20%2F%20zenodo.3703320-blue.svg?style=for-the-badge)](https://doi.org/10.5281/zenodo.3703320)

- [ESM Catalog Specification](#esm-catalog-specification)
  - [Background and Related Projects](#background-and-related-projects)
  - [The Specification](#the-specification)
  - [Intake driver: intake-esm](#intake-driver-intake-esm)

The Earth System Model Catalog specification describes a way of cataloging large datasets with a homogeneous metadata structure, such as those produced by the Coupled Model Intercomparison Project of the World Climate Research Programme.
It was designed within the Pangeo project, growing out of various ad-hoc attempts at building catalogs of convenience for CMIP6 and related dataset in the months before the [2019 CMIP6 Hackathon](https://cmip6hack.github.io).

## Background and Related Projects

![Standards](https://imgs.xkcd.com/comics/standards.png)

via <https://xkcd.com/927/>

We are guilty of creating a new standard rather than reusing one of the many reasonable alternatives already in existence.
Here we try to justify this choice.

- The [THREDDS Client Catalog Specification
  ](https://www.unidata.ucar.edu/software/tds/current/catalog/InvCatalogSpec.html)
  is an excellent, full-featured, mature specification aimed at a similar type of datasets.
  We probably could have used the THREDDS spec here, and avoided defining a new one.
  However, we are not actually planning to use THREDDS.
  The spec is in XML and is controlled by Unidata (not open for pull requests).
  For the cloud, some innovation is likely needed.
  We were looking for something simpler and more open to hacking from the community.

- [Spatiotemporal Asset Catalog](https://github.com/radiantearth/stac-spec/blob/master/README.md) was very inspirational from a technical point of view.
  We love the simplicity of their approach, with lightweight text files optimized for cloud-native operations.
  But STAC is aimed at geospatial imagery, which has slightly different attributes and challenges compared to climate model data.
  Spatiotemporal assets usually show just a small piece of the real Earth, within the recent historical period.
  Climate models generally simulate the whole planet, under hundreds or thousands of different scenarios. Not to mention weird calendars, aquaplanets, exoplanets, etc.
  We played around with STAC, but it didn't feel like the right fit.

- Our ultimate aims are similar to those of the [Earth System Grid Federation Search Tool](https://github.com/ESGF/esg-search).
  However, we are not actually running an ESGF node, so it didn't seem sensible to try to use that tool directly. We do, however, optionally reference the same [controlled vocabularies](https://github.com/WCRP-CMIP/CMIP6_CVs) as the ESGF search tool.

- [AOSPy](https://aospy.readthedocs.io/en/stable/index.html) is a workflow manager aimed at similar data ensembles.
  The data model of AOSPy is very similar to the one in ESM Catalog.
  However, the actual data catalog is described in python code, rather than text files.
  We would love to see AOSPy interoperate with ESM spec by parsing its catalogs and converting them into its objects.

- [Intake](http://intake.readthedocs.io) is python tool for cataloging and loading data, widely used in the Pangeo community.
  The catalogs are described in YAMl, and the content of these YAML files is coupled tightly to the python library.
  While intake is very convenient, we thought it was important that the catalog itself be language independent.
  We hope that, once the ESM spec is complete enough, an intake driver for parsing it should be easy to implement.

Ultimately, with sufficient time, we probably could have adopted any of the above tools and made it work for our needs.
The decision to make a new spec was ultimately driven by the timeline of the CMIP6 hackathon--it seemed like the fastest route.

## The Specification

**[collection-spec/](collection-spec/)** directory contains the esm collection core specification plus examples and information about the validation schema and validation tool.

## Intake driver: intake-esm

[Intake-esm](https://github.com/NCAR/intake-esm) is a data cataloging utility built on top of [intake](https://github.com/intake/intake), [pandas](https://pandas.pydata.org/), and [xarray](https://xarray.pydata.org/en/stable/). Intake-esm provides functionality for:

- Parsing an ESM (Earth System Model) Collection/catalog and
- Loading assets (netCDF files and/or Zarr stores) into xarray datasets.
