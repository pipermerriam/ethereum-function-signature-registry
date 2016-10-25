import logging

from huey.contrib.djhuey import db_task

from .models import Signature


logger = logging.getLogger()


@db_task()
def perform_github_import(login_or_name, repository, branch):
    logger.info("Importing github repo %s/%s/%s", login_or_name, repository, branch)
    Signature.import_from_github_repository(login_or_name, repository, branch)
