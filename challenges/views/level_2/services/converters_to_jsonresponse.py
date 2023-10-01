from django.db.models import Model, QuerySet
from django.http import JsonResponse


def jsonresponse_403():
    data = {'data': {}, 'errors': 'invalid params values'}
    return JsonResponse(data=data, status=403)


def jsonresponse_404():
    data = {'data': {}, 'errors': 'not found'}
    return JsonResponse(data=data, status=404)


def convert_queryset_to_jsonresponse(query_result: QuerySet):
    if not query_result.exists():
        return jsonresponse_404()

    objects_data = [object.to_json() for object in query_result]
    data = {'data': objects_data}
    return JsonResponse(data=data, status=200)


def convert_model_obj_to_jsonresponse(query_result: Model | None) -> JsonResponse:
    if query_result is None:
        return jsonresponse_404()

    object_data = query_result.to_json()
    data = {'data': object_data}
    return JsonResponse(data=data, status=200)
