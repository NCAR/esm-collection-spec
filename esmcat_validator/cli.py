import json
import shutil
from timeit import default_timer

import click

from .validator import EsmcatValidate


@click.command()
@click.argument('esmcat_file')
@click.option('--esmcat-spec-dirs', default=None, show_default=True)
@click.option('--version', default='master', show_default=True)
@click.option('--verbose', default=False, show_default=True)
@click.option('--timer', default=False, show_default=True)
@click.option('--log-level', default='CRITICAL', show_default=True)
def main(esmcat_file, esmcat_spec_dirs, version, verbose, timer, log_level):
    if timer:
        start = default_timer()
    esmcat = EsmcatValidate(esmcat_file, esmcat_spec_dirs, version, log_level)
    _ = esmcat.run()
    shutil.rmtree(esmcat.dirpath)

    if verbose:
        print(json.dumps(esmcat.message, indent=4))
    else:
        print(json.dumps(esmcat.status, indent=4))

    if timer:
        print(f'Validator took {default_timer() - start:.2f} seconds')


if __name__ == '__main__':
    main()
