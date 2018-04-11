import logging
import sys

from huey.contrib.djhuey import db_task

from .models import Signature


logger = logging.getLogger('bytes4.github_import')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


@db_task()
def perform_github_import(login_or_name, repository, branch):
    logger.info("Importing github repo %s/%s/%s", login_or_name, repository, branch)
    Signature.import_from_github_repository(login_or_name, repository, branch)
