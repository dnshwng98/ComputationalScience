import json

from django.http import HttpResponse
from rest_framework.decorators import api_view

from apps.spotify import business_logics


@api_view(['GET'])
def retrieve_data(request):
    return HttpResponse(business_logics.retrieve_data_from_API(json.loads(request.body)["artist"]
                                                               , json.loads(request.body)["countries"]))


@api_view(['GET'])
def color_gradation(request):
    return HttpResponse(business_logics.color_gradation())
