from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

form_date = {'text': 'ТЕКСТ'}


def test_user_create_comment(author_client, url_detail):
    cnt_before_comment = Comment.objects.count()
    response = author_client.post(url_detail, data=form_date)
    cnt_after_comment = Comment.objects.count()
    assertRedirects(response, url_detail + '#comments')
    assert cnt_after_comment - 1 == cnt_before_comment


def test_anonymus_create_comment(client, url_detail, url_login):
    cnt_before_comment = Comment.objects.count()
    response = client.post(url_detail, data=form_date)
    cnt_after_comment = Comment.objects.count()
    assertRedirects(response, f'{url_login}?next={url_detail}')
    assert cnt_before_comment == cnt_after_comment


def test_create_comment_with_bad_word(author_client, url_detail):
    bad_word_text = {
        'text': BAD_WORDS[0]
    }
    response = author_client.post(url_detail, data=bad_word_text)
    assertFormError(response, form='form', field='text', errors=WARNING)


def test_author_can_edit_comment(
        author_client, comment, url_edit,
        url_detail, author, news
):
    response = author_client.post(url_edit, data=form_date)
    assertRedirects(response, url_detail + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_date['text']
    assert comment.author == author
    assert comment.news == news


def test_author_can_delete_comment(
        author_client, comment, url_delete, url_detail
):
    cnt_before_delete = Comment.objects.count()
    response = author_client.post(url_delete)
    assertRedirects(response, url_detail + '#comments')
    cnt_after_delete = Comment.objects.count()
    assert cnt_before_delete - 1 == cnt_after_delete


def test_other_cant_edit_comment(
        admin_client, comment, url_edit
):
    response = admin_client.post(url_edit, data=form_date)
    comment_text = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == comment_text.text
    assert comment.news == comment_text.news
    assert comment.author == comment_text.author


def test_other_cant_delete_comment(
        admin_client, comment, url_delete
):
    response = admin_client.post(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
