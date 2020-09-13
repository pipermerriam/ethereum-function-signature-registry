import logging
import sys

from huey.contrib.djhuey import db_task

from .models import (
    Signature,
    EventSignature,
)
from func_sig_registry.utils.github import (
    get_repository_solidity_files,
)

logger = logging.getLogger('bytes4.github_import')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


@db_task()
def perform_github_import(login_or_name, repository, branch):
    logger.info("Importing github repo %s/%s/%s", login_or_name,
                repository, branch)
    for file_path in get_repository_solidity_files(login_or_name, repository, branch):
            logger.info("importing solidity file: %s", file_path)
            with open(file_path) as solidity_file:
                try:
                    Signature.import_from_solidity_file(solidity_file)
                    EventSignature.import_from_solidity_file(solidity_file)
                except UnicodeDecodeError:
                    logger.error('unicode error reading solidity file: %s',
                                 file_path)
