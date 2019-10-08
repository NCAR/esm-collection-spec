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


class Esmcat:
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


class EsmcatValidate:
    def __init__(self, esmcat_file, esmcat_spec_dirs=None, version='master', log_level='CRITICAL'):
        """ Validate an ESMCat file
        Parameters
        ----------
        esmcat_file : str
              File to validate
        esmcat_spec_dirs : list
            List of local specification directories to check for JSON schema files.
        version : str, defaults to `master`
            ESMCat version to validate against. Uses github tags from the esm-collection-repo. e.g.: v0.1.0
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

        logging.info('ESMCat Validator Started.')
        self.esmcat_version = version
        self.esmcat_file = esmcat_file.strip()
        self.dirpath = tempfile.mkdtemp()
        self.esmcat_spec_dirs = self.check_none(esmcat_spec_dirs)

        self.message = []
        self.status = {'collections': {'valid': 0, 'invalid': 0}, 'unknown': 0}

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
        ESMCat spec in json format
        """
        spec_name = spec

        if self.esmcat_spec_dirs is None:
            try:
                logging.debug('Gathering ESMCat specs from remote.')
                url = getattr(Esmcat, f'{spec_name}_schema_url')
                spec = requests.get(url(self.esmcat_version)).json()
                valid_dir = True

            except Exception:
                logger.exception('ESMCat Download Error')
                raise VersionException(f'Could not download ESMCat specification')
        else:
            valid_dir = False
            for esmcat_spec_dir in self.esmcat_spec_dirs:
                spec_file = Path(esmcat_spec_dir) / spec_name / '.json'
                if spec_file.is_file():
                    valid_dir = True
                    try:
                        logging.debug('Gather ESMCat specs from local directory.')
                        with open(spec_file, 'r') as f:
                            spec = json.load(f)

                    except FileNotFoundError:
                        try:
                            logger.critical(
                                f'Houston, we have a problem! Could not find spec file {spec_file}'
                            )
                            url = getattr(Esmcat, f'{spec_name}_schema_url')
                            spec = requests.get(url(self.esmcat_version)).json()

                        except:
                            logger.exception(
                                'The ESMCat specification file does not exist or does not match the ESMCat file you are trying '
                                'to validate. Please check your esmcat_spec_dirs path.'
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
                'The ESMCat specification file does not exist or does not match the ESMCat file you are trying '
                'to validate. Please check your esmcat_spec_dirs path.'
            )
            sys.exit(1)

        return spec

    def validate_json(self, content, schema):
        """ Validate ESMCat
        Parameters
        ----------
        content : dict
             input ESMCat file content
        schema : dict
             schema of ESMCat

        Returns
        -------
        validation message
        """
        try:
            logging.info('Validating ESMCat')
            validate(content, schema)
            return True, None
        except ValidationError as e:
            logger.warning('ESMCat Validation Error')
            return False, f'{e.message} of {list(e.path)}'

        except Exception as e:
            logger.exception('ESMCat error')
            return False, f'{e}'

    @staticmethod
    def _update_status(old_status, new_status):
        old_status['collections']['valid'] += new_status['collections']['valid']
        old_status['collections']['invalid'] += new_status['collections']['invalid']
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
        """ Fetch and parse ESMCat file.

        Parameters
        ----------
        input_path : str
             ESMCat file to get and read

        Returns
        -------
        content or error message
        """

        err_message = {}
        data = None

        try:
            if self.is_valid_url(input_path):
                logger.info('Loading ESMCat from URL')
                resp = requests.get(input_path)
                data = resp.json()
            else:
                with open(input_path) as f:
                    logger.info('Loading ESMCat from filesystem')
                    data = json.load(f)

        except JSONDecodeError:
            logger.exception('JSON Decode Error')
            err_message['valid_esmcol'] = False
            err_message['error_type'] = 'InvalidJSON'
            err_message['error_message'] = f'{input_path} is not Valid JSON'

        except FileNotFoundError:
            logger.exception('ESMCat File Not Found')
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
        status = {'collections': {'valid': 0, 'invalid': 0}, 'unknown': 0}

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
            message['valid_esmcol'] = is_valid_esmcol
            message['error_message'] = err_message

            if message['valid_esmcol']:
                status['collections']['valid'] = 1

            else:
                status['collections']['invalid'] = 1

        message['path'] = esmcol_path
        return message, status

    def run(self):
        """ Entry point

        Returns
        -------
        message : json
        """
        message, status = self._validate(self.esmcat_file)
        self.status = self._update_status(self.status, status)
        self.message.append(message)

        return json.dumps(self.message)
