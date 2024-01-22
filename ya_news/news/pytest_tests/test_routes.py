from http import HTTPStatus

import pytest

from django.urls import reverse

from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

pytestmark = pytest.mark.django_db
HTTP_OK = HTTPStatus.OK
HTTP_NF = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'url',
    (
        (lf('url_edit')),
        (lf('url_delete'))
    )
)
def test_comment_edit_delete_redirect(client, url):
    response = client.get(url)
    login = reverse('users:login')
    assertRedirects(response, f'{login}?next={url}')


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (lf('url_edit'), lf(
            'author_client'), HTTP_OK),
        (lf('url_edit'), lf(
            'admin_client'), HTTP_NF),
        (lf('url_delete'), lf(
            'author_client'), HTTP_OK),
        (lf('url_delete'), lf(
            'admin_client'), HTTP_NF),
        (lf('url_home'),
         lf('client'), HTTP_OK),
        (lf('url_detail'),
         lf('client'), HTTP_OK),
        (lf('url_signup'), lf('client'),
         HTTP_OK),
        (lf('url_login'), lf('client'), HTTP_OK),
        (lf('url_logout'), lf('client'), HTTP_OK)
    )
)
def test_avalible_for_anonym_and_edit_delete(
        reverse_url, parametrized_client, status
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status
