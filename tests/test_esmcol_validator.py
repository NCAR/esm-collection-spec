from esmcol_validator import validator


def _run_validate(url, esmcol_spec_dirs=None, version='master', log_level='DEBUG'):
    esmcol = validator.EsmcolValidate(url, esmcol_spec_dirs, version, log_level)
    esmcol.run()
    return esmcol


def test_collection_remote():
    esmcol = _run_validate(
        'https://raw.githubusercontent.com/NCAR/esm-collection-spec/master/collection-spec/examples/sample-pangeo-cmip6-collection.json'
    )
    expected = {'collections': {'valid': 1, 'invalid': 0}, 'unknown': 0}
    assert esmcol.status == expected
