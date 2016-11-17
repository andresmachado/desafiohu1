import json
from datetime import datetime

from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView
from django.core import serializers
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Q

from .models import Hotel


# Create your views here.


class IndexView(TemplateView):
    template_name='hotels/search.html'


def list_hotels_json(request):

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


def search_hotels_result(request, template_name='hotels/results.html'):
    if request.POST:
        location = request.POST.get('location', None)
        checkin = request.POST.get('checkin', None)
        checkout = request.POST.get('checkout', None)
        no_date = request.POST.get('no-dates', None)
        
        hotels = Hotel.objects.all()
        
        if location:
            hotels = hotels.filter(Q(name__icontains = location) | Q(city__icontains = location))
            if checkin:
                checkin = datetime.strptime(checkin, '%d/%m/%Y').strftime('%Y-%m-%d')
                if checkout:
                    checkout = datetime.strptime(checkout, '%d/%m/%Y').strftime('%Y-%m-%d')
                    hotels = hotels.filter(disponibility__date__gte=checkin, disponibility__date__lte=checkout, disponibility__avaiable=True).distinct()
                else:
                    hotels = hotels.filter(disponibility__date__gte=checkin, disponibility__avaiable=True).distinct()
        
        context = {
            'hotels': hotels,
            'checkin': checkin,
            'checkout': checkout
        }
    else:
        raise Http404
    return render(request, template_name, context)