from huey.contrib.djhuey import db_task

from .models import Signature


@db_task()
def perform_github_import(username, repository, branch):
    Signature.import_from_github_repository(username, repository, branch)
