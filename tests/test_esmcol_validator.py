import os

import pytest

from esmcol_validator import validator

here = os.path.abspath(os.path.dirname(__file__))


def _run_validate(url, esmcol_spec_dirs=None, version='master', log_level='DEBUG'):
    esmcol = validator.EsmcolValidate(url, esmcol_spec_dirs, version, log_level)
    esmcol.run()
    return esmcol


def test_good_collection_local():
    esmcol = _run_validate(os.path.join(here, 'test_data/good_collection.json'))
    expected = {
        'collections': {'valid': 1, 'invalid': 0},
        'catalog_files': {'valid': 1, 'invalid': 0},
        'unknown': 0,
    }
    assert esmcol.status == expected


def test_bad_spec():
    with pytest.raises(SystemExit) as e:
        _ = _run_validate(
            os.path.join(here, 'test_data/good_collection.json'), esmcol_spec_dirs='./'
        )
        assert e.value.code == 1


def test_bad_catalog_file():
    esmcol = _run_validate(os.path.join(here, 'test_data/bad_collection.json'))
    assert esmcol.status['catalog_files']['invalid'] == 1


def test_catalog_file_not_found():
    esmcol = _run_validate(
        'https://raw.githubusercontent.com/NCAR/esm-collection-spec/master/collection-spec/examples/sample-glade-cmip6-netcdf-collection.json'
    )
    expected = {
        'collections': {'valid': 1, 'invalid': 0},
        'catalog_files': {'valid': 0, 'invalid': 1},
        'unknown': 0,
    }
    assert esmcol.status == expected
