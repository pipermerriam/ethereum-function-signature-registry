import pytest

from func_sig_registry.utils.github import (
    get_repository_solidity_files,
)


@pytest.mark.skip(reason='makes an http request')
def test_getting_repository_solidity_files():
    file_list = list(get_repository_solidity_files(
        'pipermerriam',
        'ethereum-alarm-clock',
    ))
    assert len(file_list) == 24
