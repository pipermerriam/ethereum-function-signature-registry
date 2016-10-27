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
