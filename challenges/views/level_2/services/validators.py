from challenges.models import Laptop, Post


def validate_min_price(min_price_str: str | None) -> int | None:
    if not min_price_str.isdigit():
        return None

    min_price = int(min_price_str)
    return min_price if min_price >= 0 else None


def validate_brand(brand: str | None) -> str | None:
    possible_brands_dict = {brand[1]: brand[0] for brand in Laptop.brand.field.choices}

    return possible_brands_dict.get(brand.capitalize(), None)


def validate_post_categories(query_categories: str) -> list:
    query_categories = list(map(lambda x: x.capitalize(), query_categories.split(',')))
    possible_categories = {cat[1]: cat[0] for cat in Post.category.field.choices}
    return [possible_categories.get(cat) for cat in query_categories if possible_categories.get(cat)]


def validate_last_days(last_days: str) -> int | None:
    try:
        last_days = int(last_days)
    except (ValueError, TypeError):
        return None

    return last_days if last_days > 0 else None
