# ESM Catalog Spec

The Earth System Model Catalog specification describes a way of cataloging large datasets with a homogeneous metadata structure, such as those produced by the Coupled Model Intercomparison Project of the World Climate Research Programme.
It was designed within the Pangeo project, growing out of various ad-hoc attempts at building catalogs of convenience for CMIP6 and related dataset in the months before the [2019 CMIP6 Hackathon](https://cmip6hack.github.io).

## Background and Related Projects

![Standards](https://imgs.xkcd.com/comics/standards.png)

via <https://xkcd.com/927/>

We are guilty of creating a new standard rather than reusing one of the many reasonable alternatives already in existence.
Here we try to justify this choice.

- The [THREDDS Client Catalog Specification
](https://www.unidata.ucar.edu/software/tds/current/catalog/InvCatalogSpec.html)
  is a excellent, full-featured, mature specification aimed at a similar type of datasets.
  We probably could have used the THREDDS spec here, and avoided defining a new one.
  However, we are not actually planning to use THREDDS
  It is in XML and is controlled by Unidata.
  For the cloud, some innovation is likely needed.
  We were looking for something simpler and more open to hacking from the community.

- [Spatiotemporal Asset Catalog](https://github.com/radiantearth/stac-spec/blob/master/README.md) was very inspirational from a technical point of view.
  We love the simplicity of their approach, with lightweight text files optimized for cloud-native operations.
  But STAC is aimed at geospatial imagery, which has slightly different attributes and challenges compared to climate model data.
  Spatiotemporal assets usually show just a small piece of the real Earth, within the recent historical period.
  Climate models generally simulate the whole planet, under hundreds or thousands of different scenarios. Not to mention weird calendars, aquaplanets, exoplanets, etc.
  We played around with STAC, but it didn't feel like the right fit.

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

### Catalog Descriptor

### Catalog

### Data Files
