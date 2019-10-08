from esmcat_validator import validator


def _run_validate(url, esmcat_spec_dirs=None, version='master', log_level='DEBUG'):
    esmcat = validator.EsmcatValidate(url, esmcat_spec_dirs, version, log_level)
    esmcat.run()
    return esmcat


def test_collection_remote():
    esmcat = _run_validate(
        'https://raw.githubusercontent.com/NCAR/esm-collection-spec/master/collection-spec/examples/sample-pangeo-cmip6-collection.json'
    )
    expected = {'collections': {'valid': 1, 'invalid': 0}, 'unknown': 0}
    assert esmcat.status == expected
