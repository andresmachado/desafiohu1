import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core import serializers
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Q

from .models import Hotel


# Create your views here.


class IndexView(TemplateView):
    template_name='hotels/base.html'


def list_hotels(request):
    response = []
    q = request.GET.get('term', '')

    qs = Hotel.objects.all()

    if q:
        qs = qs.filter(
            Q(name__istartswith = q) |
            Q(city__istartswith = q)
        )

    for hotel in qs:
        hotel_result = {}
        hotel_result['id'] = hotel.id
        hotel_result['name'] = hotel.name
        hotel_result['city'] = hotel.city
        response.append(hotel_result)

    data = json.dumps(response, ensure_ascii=False)
    return JsonResponse(data, safe=False)