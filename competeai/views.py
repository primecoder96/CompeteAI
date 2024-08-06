from django.http import HttpResponse
from django.shortcuts import render
import google.generativeai as genai
from decouple import config  # Import config from python-decouple
import json
from django.views.decorators.csrf import csrf_exempt
from .models import DirectRating, InDirectRating
from .services.service import get_report,get_org_offerings,get_industry_category

GLOBAL_VAR = None


def describe_product(request):
    return render(request, 'product.html')


def home(request):
    return render(request, 'home.html')


@csrf_exempt
def report(request):
    data = json.loads(request.body)
    phrase = data.get("description")
    industry = get_industry_category(phrase)
    industry = json.dumps(industry)
    GLOBAL_VAR = get_report(phrase)
    if len(GLOBAL_VAR) != 0:
        response = HttpResponse(status=200)
        response.set_cookie('key', GLOBAL_VAR)
        response.set_cookie('industry',industry)
        return response
    else:
        return HttpResponse(status=500)


def render_stat(request):
    json_string = request.COOKIES.get('key')
    industry = json.loads(request.COOKIES.get('industry'))
    print("we are printing json")
    print(industry)
    context = {'json_string': json_string,'industry': industry["result"]}
    return render(request, 'report.html', context)

def set_cookie(request):
    response = HttpResponse("Cookie Set")
    response.set_cookie('key', GLOBAL_VAR)
    return response


def test(request):
    data = get_org_offerings(request)
    data = json.dumps(data)
    context = {'json_string': data}
    return render(request, 'org_offering.html', context)