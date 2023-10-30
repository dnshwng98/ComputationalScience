import json

from django.http import HttpResponse
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view

from apps.earthquake import business_logics


@api_view(['GET'])
def check(request):
    business_logics.test()

    # Path to your pre-prepared HTML file
    html_file_path = 'main/file.html'

    # Return the HTML content as a response
    return TemplateResponse(request, html_file_path, content_type='text/html')


@api_view(['GET'])
def retrieve_data(request):
    return HttpResponse(business_logics.retrieve_data_from_web(json.loads(request.body)["target"]))


@api_view(['GET'])
def collect_new_data(request):
    return HttpResponse(business_logics.collect_new_data(json.loads(request.body)["target"]))


@api_view(['GET'])
def check_the_amount_of_new_data_available(request):
    return HttpResponse(business_logics.check_the_amount_of_new_data_available(json.loads(request.body)["target"]))