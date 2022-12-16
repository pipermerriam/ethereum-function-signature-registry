import os
import tempfile
import tarfile

import requests


ARCHIVE_URL = "https://github.com/{username}/{repository}/archive/{branch}.tar.gz"


def get_repository_solidity_files(username, repository, branch='master'):
    archive_url = ARCHIVE_URL.format(
        username=username,
        repository=repository,
        branch=branch,
    )
    with tempfile.TemporaryDirectory() as base_dir:
        response = requests.get(archive_url, stream=True)
        response.raise_for_status()

        archive_path = os.path.join(base_dir, '{branch}.tar.gz'.format(branch=branch))

        with open(archive_path, 'wb') as archive_file:
            for chunk in response:
                archive_file.write(chunk)

        extract_path = os.path.join(base_dir, 'files')
        os.mkdir(extract_path)

        with tarfile.open(archive_path) as archive_file:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(archive_file, extract_path)

        for dirpath, _, filenames in os.walk(extract_path):
            for filename in filenames:
                _, extension = os.path.splitext(filename)
                if extension == ".sol":
                    full_path = os.path.join(dirpath, filename)
                    yield full_path
