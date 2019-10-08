import os

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
