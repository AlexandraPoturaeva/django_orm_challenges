"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from datetime import datetime, timedelta
from django.http import HttpRequest, JsonResponse

from challenges.models import Post
from challenges.views.level_2.services.converters_to_jsonresponse import convert_queryset_to_jsonresponse, jsonresponse_403
from challenges.views.level_2.services.validators import validate_post_categories, validate_last_days


def last_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    last_three_posts = Post.objects.all()[:3]
    return convert_queryset_to_jsonresponse(query_result=last_three_posts)


def posts_search_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    query = request.GET.get('query')

    if not query:
        return jsonresponse_403()

    query_result = Post.objects.filter(text__icontains=query)
    return convert_queryset_to_jsonresponse(query_result=query_result)


def untagged_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    untagged_posts = Post.objects.filter(category__isnull=True).order_by('author_name', '-created_at')
    return convert_queryset_to_jsonresponse(query_result=untagged_posts)


def categories_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    raw_query_categories = request.GET.get('categories')

    if raw_query_categories:
        query_categories = validate_post_categories(raw_query_categories)
    else:
        return jsonresponse_403()

    query_result = Post.objects.filter(category__in=query_categories)
    return convert_queryset_to_jsonresponse(query_result=query_result)


def last_days_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    raw_last_days = request.GET.get('last_days')
    last_days = validate_last_days(raw_last_days)

    if not last_days:
        return jsonresponse_403()

    day_start = datetime.today() - timedelta(days=last_days)
    query_result = Post.objects.filter(published_at__gt=day_start)
    return convert_queryset_to_jsonresponse(query_result=query_result)
