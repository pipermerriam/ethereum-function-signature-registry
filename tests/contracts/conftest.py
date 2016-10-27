import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def test_contract_factories(project):
    from solc import compile_files
    from populus.utils.filesystem import (
        recursive_find_files,
    )
    from populus.compilation import (
        find_project_contracts,
    )

    base_tests_dir = os.path.dirname(__file__)

    test_source_files = [
        os.path.relpath(source_path, project.project_dir)
        for source_path in recursive_find_files(base_tests_dir, 'Test*.sol')
    ]
    all_source_files = test_source_files + list(find_project_contracts(
        project.project_dir, project.contracts_dir,
    ))
    compiled_contracts = compile_files(all_source_files)
    for contract_name, contract_data in compiled_contracts.items():
        project.compiled_contracts.setdefault(contract_name, contract_data)


@pytest.fixture()
def signature_db(chain):
    return chain.get_contract('SignatureDB')


@pytest.fixture()
def SignatureDB(signature_db):
    return type(signature_db)


@pytest.fixture()
def test_string_lib(chain):
    return chain.get_contract('TestStringLib')


@pytest.fixture()
def TestStringLib(test_string_lib):
    return type(test_string_lib)


@pytest.fixture()
def test_array_lib(chain):
    return chain.get_contract('TestArrayLib')


@pytest.fixture()
def TestArrayLib(test_array_lib):
    return type(test_array_lib)


@pytest.fixture()
def test_argument_lib(chain):
    return chain.get_contract('TestArgumentLib')


@pytest.fixture()
def TestArgumentLib(test_argument_lib):
    return type(test_argument_lib)


@pytest.fixture()
def test_canonical_signature_lib(chain):
    return chain.get_contract('TestCanonicalSignatureLib')


@pytest.fixture()
def TestCanonicalSignatureLib(test_canonical_signature_lib):
    return type(test_canonical_signature_lib)
