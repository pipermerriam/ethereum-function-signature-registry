import os

import pytest
import factory

from django_webtest import (
    WebTest as BaseWebTest,
    DjangoTestApp
)

from rest_framework.test import APIClient


@pytest.fixture()  # NOQA
def factories(transactional_db):
    from factories import (  # NOQA
        SignatureFactory,
        BytesSignatureFactory,
    )

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.Factory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models_no_db():
    from django.apps import apps

    dict_ = {M._meta.object_name: M for M in apps.get_models()}

    return type(
        'models',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models(models_no_db, transactional_db):
    return models_no_db


class WebTest(BaseWebTest):
    app_class = DjangoTestApp


@pytest.fixture()  # NOQA
def webtest_client(transactional_db):
    web_test = WebTest(methodName='__call__')
    web_test()
    return web_test.app


@pytest.fixture()
def api_client(transactional_db):
    """
    A rest_framework api test client not auth'd.
    """
    client = APIClient()
    return client


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
