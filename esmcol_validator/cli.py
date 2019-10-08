import json
import shutil
from timeit import default_timer

import click

from .validator import EsmcolValidate


@click.command()
@click.argument('esmcol_file')
@click.option('--esmcol-spec-dirs', default=None, show_default=True)
@click.option('--version', default='master', show_default=True)
@click.option('--verbose', default=False, show_default=True, is_flag=True)
@click.option('--timer', default=False, show_default=True, is_flag=True)
@click.option('--log-level', default='CRITICAL', show_default=True)
def main(esmcol_file, esmcol_spec_dirs, version, verbose, timer, log_level):
    if timer:
        start = default_timer()
    esmcol = EsmcolValidate(esmcol_file, esmcol_spec_dirs, version, log_level)
    _ = esmcol.run()
    shutil.rmtree(esmcol.dirpath)

    if verbose:
        print(json.dumps(esmcol.message, indent=4))
    else:
        print(json.dumps(esmcol.status, indent=4))

    if timer:
        print(f'Validator took {default_timer() - start:.2f} seconds')


if __name__ == '__main__':
    main()
