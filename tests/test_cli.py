import os
import subprocess

here = os.path.abspath(os.path.dirname(__file__))


def test_cli_runner():
    esmcol_file = os.path.join(here, 'test_data/good_collection.json')
    p = subprocess.Popen(
        ['esmcol-validator', esmcol_file], stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    p.communicate()
    assert p.returncode == 0


def test_empty_input():
    p = subprocess.Popen(['esmcol-validator'], stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p.communicate()
    assert p.returncode != 0
