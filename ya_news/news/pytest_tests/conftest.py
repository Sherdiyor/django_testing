from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

User = get_user_model()
HOME_URL = 'news:home'
DETAIL_URL = 'news:detail'


@pytest.fixture
def news_date():
    today = datetime.today()
    ten_news = []
    for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title=f'Новость № {i}',
            text='ТЕКСТ',
            date=today - timedelta(days=i)
        )
        ten_news.append(news)
    News.objects.bulk_create(ten_news)


@pytest.fixture
def author():
    return User.objects.create(username='test')


@pytest.fixture
def news():
    return News.objects.create(
        title='test',
        text='test'
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        text='test',
        news=news,
        author=author
    )


@pytest.fixture
def comment_date(author, news):
    now = timezone.now()
    for i in range(3):
        comment = Comment.objects.create(
            text=f'Комментарий № {i}',
            news=news,
            author=author
        )
        comment.created = now + timedelta(hours=i)
        comment.save()


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def url_detail(news):
    return reverse(DETAIL_URL, args=(news.id,))


@pytest.fixture
def url_home():
    return reverse(HOME_URL)


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_signup():
    return reverse('users:signup')


@pytest.fixture
def url_logout():
    return reverse('users:logout')
