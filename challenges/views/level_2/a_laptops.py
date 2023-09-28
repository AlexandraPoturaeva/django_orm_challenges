"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse, JsonResponse
from challenges.models import Laptop
from challenges.views.level_2.utils import convert_query_result_to_jsonresponse, valid_brand, valid_min_price


def laptop_details_view(request: HttpRequest, laptop_id: int) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    laptop = Laptop.objects.filter(id=laptop_id).first()

    return convert_query_result_to_jsonresponse(query_result=laptop)


def laptop_in_stock_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops = Laptop.objects.filter(stock_amount__gt=0).order_by('-created_at')

    return convert_query_result_to_jsonresponse(query_result=laptops)


def laptop_filter_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    brand = request.GET.get('brand')
    min_price = request.GET.get('price')

    min_price = valid_min_price(min_price)
    brand = valid_brand(brand)

    if not min_price and brand:
        return HttpResponse(status=403)

    laptops = Laptop.objects.filter(brand=brand, price_rub__lte=min_price)
    return convert_query_result_to_jsonresponse(query_result=laptops)


def last_laptop_details_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    try:
        last_laptop = Laptop.objects.latest()
    except Laptop.DoesNotExist:
        return HttpResponse(status=404)

    return convert_query_result_to_jsonresponse(query_result=last_laptop)
