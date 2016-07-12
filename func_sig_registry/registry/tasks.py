import logging

from huey.contrib.djhuey import db_task

from .models import Signature


logger = logging.getLogger()


@db_task()
def perform_github_import(username, repository, branch):
    logger.info("Importing github repo %s/%s/%s", username, repository, branch)
    Signature.import_from_github_repository(username, repository, branch)
