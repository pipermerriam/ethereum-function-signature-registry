import pytest


@pytest.fixture()
def char_lib(chain):
    return chain.get_contract('CharLib')


@pytest.fixture()
def CharLib(char_lib):
    return type(char_lib)


@pytest.fixture()
def string_lib(chain):
    return chain.get_contract('StringLib')


@pytest.fixture()
def StringLib(string_lib):
    return type(string_lib)
