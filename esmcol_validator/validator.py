import json
import logging
import sys
import tempfile
from functools import lru_cache
from json.decoder import JSONDecodeError
from pathlib import Path
from urllib.parse import urlparse

import requests
from jsonschema import ValidationError, validate

logger = logging.getLogger(__name__)


class Esmcol:
    def __init__(self, version='master', input_type='', filename=''):
        self.input_type = input_type
        self.filename = filename
        self.version = version
        self._determine_version()

    def _determine_version(self):
        git_base_url = f'https://raw.githubusercontent.com/NCAR/esm-collection-spec/{self.version}'
        self.COLLECTION_URL = f'{git_base_url}/collection-spec/{self.input_type}/{self.filename}'

    @classmethod
    def collection_schema_url(cls, version, filename='collection.json'):
        return cls(version, 'json-schema', filename).COLLECTION_URL


class VersionException(Exception):
    pass


class EsmcolValidate:
    def __init__(self, esmcol_file, esmcol_spec_dirs=None, version='master', log_level='CRITICAL'):
        """ Validate an ESMCol file
        Parameters
        ----------
        esmcol_file : str
              File to validate
        esmcol_spec_dirs : list
            List of local specification directories to check for JSON schema files.
        version : str, defaults to `master`
            ESMcat version to validate against. Uses github tags from the esm-collection-repo. e.g.: v0.1.0
        log_level : str
            Level of logging to report
        """

        numeric_log_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_log_level, int):
            raise ValueError(f'Invalid log level: {log_level}')

        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(thread)d : %(message)s',
            datefmt='%m/%d/%Y %H:%M:%S',
            level=numeric_log_level,
        )

        logging.info('ESMCol Validator Started.')
        self.esmcat_version = version
        self.esmcol_file = esmcol_file.strip()
        self.dirpath = tempfile.mkdtemp()
        self.esmcol_spec_dirs = self.check_none(esmcol_spec_dirs)

        self.message = []
        self.status = {
            'collections': {'valid': 0, 'invalid': 0},
            'catalog_files': {'valid': 0, 'invalid': 0},
            'unknown': 0,
        }

    @staticmethod
    def check_none(input):
        """ Checks if the string is None
        Parameters
        ----------
        input : str
            Input string to check
        """
        if input == 'None':
            return None
        try:
            return input.split(',')
        except AttributeError:
            return input
        except Exception:
            logger.warning('Could not find input file')

    @lru_cache(maxsize=48)
    def fetch_spec(self, spec):
        """ Get the spec file and cache it.
        Parameters
        ----------
        spec : str
           Name of spec to get

        Returns
        -------
        ESMCol spec in json format
        """
        spec_name = spec

        if self.esmcol_spec_dirs is None:
            try:
                logging.debug('Gathering ESMCol specs from remote.')
                url = getattr(Esmcol, f'{spec_name}_schema_url')
                spec = requests.get(url(self.esmcat_version)).json()
                valid_dir = True

            except Exception:
                logger.exception('ESMCol Download Error')
                raise VersionException(f'Could not download ESMCol specification')
        else:
            valid_dir = False
            for esmcol_spec_dir in self.esmcol_spec_dirs:
                spec_file = Path(esmcol_spec_dir) / spec_name / '.json'
                if spec_file.is_file():
                    valid_dir = True
                    try:
                        logging.debug('Gather ESMCol specs from local directory.')
                        with open(spec_file, 'r') as f:
                            spec = json.load(f)

                    except FileNotFoundError:
                        try:
                            logger.critical(
                                f'Houston, we have a problem! Could not find spec file {spec_file}'
                            )
                            url = getattr(Esmcol, f'{spec_name}_schema_url')
                            spec = requests.get(url(self.esmcat_version)).json()

                        except:
                            logger.exception(
                                'The ESMCol specification file does not exist or does not match the ESMCol file you are trying '
                                'to validate. Please check your esmcol_spec_dirs path.'
                            )
                            sys.exit(1)
                    except Exception as e:
                        logging.exception(e)

        if valid_dir:
            file_name = (
                Path(self.dirpath) / f"{spec_name}_{self.esmcat_version.replace('.','_')}.json"
            )
            with open(file_name, 'w') as fp:
                logging.debug(f'Copying {spec_name} spec from local file to cache')
                fp.write(json.dumps(spec))
        else:
            logger.exception(
                'The ESMCol specification file does not exist or does not match the ESMCol file you are trying '
                'to validate. Please check your esmcol_spec_dirs path.'
            )
            sys.exit(1)

        return spec

    def validate_json(self, content, schema):
        """ Validate ESMCol
        Parameters
        ----------
        content : dict
             input ESMCol file content
        schema : dict
             schema of ESMCol

        Returns
        -------
        validation message
        """
        try:
            logging.info('Validating ESMCol')
            validate(content, schema)
            return True, None
        except ValidationError as e:
            logger.warning('ESMCol Validation Error')
            return False, f'{e.message} of {list(e.path)}'

        except Exception as e:
            logger.exception('ESMCol error')
            return False, f'{e}'

    def validate_csv(self, content):
        """
        Validate ESMCat file
        Parameters
        ----------
        content : dict
             input ESMCol file content

        Returns
        -------
        validation message
        """
        import pandas as pd

        catalog_file = content['catalog_file']
        attributes = content['attributes']
        assets = content['assets']
        if ('format' in assets) and ('format_column_name' in assets):
            return False, "'format' and 'format_column_name' are mutually exclusive"

        columns = [item['column_name'] for item in attributes]
        if 'format_column_name' in assets:
            columns.append(assets['format_column_name'])

        columns.append(assets['column_name'])

        try:
            df = pd.read_csv(catalog_file, index_col=0)
            x = set(columns)
            y = set(df.columns)

            if x.issubset(y) and not y.issubset(x):
                message = f'Catalog file: {catalog_file} contains { y - x} columns that are not found in esm collection spec.'
                return False, message

            else:
                return True, None

        except FileNotFoundError:
            logger.exception(f'Catalog File: {catalog_file} does not exist.')
            return False, f'Could not read catalog file: {catalog_file}'
        except Exception as e:
            logger.exception('ESMCat file error')
            return False, f'{e}'

    @staticmethod
    def _update_status(old_status, new_status):
        old_status['collections']['valid'] += new_status['collections']['valid']
        old_status['collections']['invalid'] += new_status['collections']['invalid']
        old_status['catalog_files']['valid'] += new_status['catalog_files']['valid']
        old_status['catalog_files']['invalid'] += new_status['catalog_files']['invalid']
        old_status['unknown'] += new_status['unknown']
        return old_status

    @staticmethod
    def is_valid_url(url):
        """ Check if path is URL or not

        Parameters
        ----------
        url : str
            path to check

        Returns
        -------
        boolean
        """
        try:
            result = urlparse(url)
            return result.scheme and result.netloc and result.path
        except Exception:
            return False

    def fetch_and_parse_file(self, input_path):
        """ Fetch and parse ESMCol file.

        Parameters
        ----------
        input_path : str
             ESMCol file to get and read

        Returns
        -------
        content or error message
        """

        err_message = {}
        data = None

        try:
            if self.is_valid_url(input_path):
                logger.info('Loading ESMCol from URL')
                resp = requests.get(input_path)
                data = resp.json()
            else:
                with open(input_path) as f:
                    logger.info('Loading ESMCol from filesystem')
                    data = json.load(f)

        except JSONDecodeError:
            logger.exception('JSON Decode Error')
            err_message['valid_esmcol'] = False
            err_message['error_type'] = 'InvalidJSON'
            err_message['error_message'] = f'{input_path} is not Valid JSON'

        except FileNotFoundError:
            logger.exception('ESMCol File Not Found')
            err_message['valid_esmcol'] = False
            err_message['error_type'] = 'FileNotFoundError'
            err_message['error_message'] = f'{input_path} cannot be found'

        return data, err_message

    def _validate(self, esmcol_path):
        Collection_Fields = [
            'esmcat_version',
            'id',
            'description',
            'catalog_file',
            'attributes',
            'assets',
        ]

        message = {}
        status = {
            'collections': {'valid': 0, 'invalid': 0},
            'catalog_files': {'valid': 0, 'invalid': 0},
            'unknown': 0,
        }

        esmcol_content, err_message = self.fetch_and_parse_file(esmcol_path)
        if err_message:
            status['unkown'] = 1
            return err_message, status

        if type(esmcol_content) is dict and any(
            field in Collection_Fields for field in esmcol_content.keys()
        ):
            logger.info('ESMCol is a Collection')
            is_valid_esmcol, err_message = self.validate_json(
                esmcol_content, self.fetch_spec('collection')
            )

            is_valid_esmcat, cat_err_message = self.validate_csv(esmcol_content)
            message['valid_esmcol'] = is_valid_esmcol
            message['error_message'] = err_message
            message['valid_esmcat'] = is_valid_esmcat
            message['cat_error_message'] = cat_err_message

            if message['valid_esmcol']:
                status['collections']['valid'] = 1

            else:
                status['collections']['invalid'] = 1

            if message['valid_esmcat']:
                status['catalog_files']['valid'] = 1
            else:
                status['catalog_files']['invalid'] = 1

        message['path'] = esmcol_path
        print(status)
        return message, status

    def run(self):
        """ Entry point

        Returns
        -------
        message : json
        """
        message, status = self._validate(self.esmcol_file)
        self.status = self._update_status(self.status, status)
        self.message.append(message)

        return json.dumps(self.message)
