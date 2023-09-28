from django.db.models import Model, QuerySet
from django.http import JsonResponse

from challenges.models import Laptop, Post


def valid_min_price(min_price: str | None) -> int | None:
    try:
        min_price = int(min_price)
    except (ValueError, TypeError):
        return None

    return min_price if min_price >= 0 else None


def valid_brand(brand: str | None) -> str | None:
    possible_brands_dict = {brand[1]: brand[0] for brand in Laptop.brand.field.choices}

    return possible_brands_dict.get(brand.capitalize(), None)


def convert_query_result_to_jsonresponse(query_result: Model | QuerySet | None) -> JsonResponse:
    if query_result is None or not query_result.exists():
        data = {'data': {}, 'errors': 'Page not found'}
        status = 404

    else:
        status = 200
        if type(query_result) == Model:
            objects_data = query_result.to_json()

        else:
            objects_data = [object.to_json() for object in query_result]

        data = {'data': objects_data}

    return JsonResponse(data=data, status=status)


def valid_post_categories(query_categories: str) -> list:
    query_categories = list(map(lambda x: x.capitalize(), query_categories.split(',')))
    possible_categories = {cat[1]: cat[0] for cat in Post.category.field.choices}

    return [possible_categories.get(cat) for cat in query_categories if possible_categories.get(cat)]


def valid_last_days(last_days: str) -> int | None:
    try:
        last_days = int(last_days)
    except (ValueError, TypeError):
        return None

    return last_days if last_days > 0 else None