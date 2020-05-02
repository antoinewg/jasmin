from django.shortcuts import render
from django.http import HttpResponse

from equities.models import Stock


def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def stocks(request):
    stocks = Stock.objects.all()
    return render(request, "stocks.html", locals())
