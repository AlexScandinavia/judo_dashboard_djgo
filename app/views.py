from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import pandas as pd
import numpy as np
from django.http import JsonResponse


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')


def main_chart_data(request, type="medals"):

    if type=="medals":
        chart = {
            'xAxis': {'categories': [2014, 2015, 2016, 2017, 2018, 2019, 2020]},
            'yAxis': {"title": {"text": 'Total number of medals/year'}},
            'series': [{
                "name": '1st place',
                "data": [0, 0, 0, 1, 2, 5, 6]
            }, {
                "name": '2nd place',
                "data": [0, 0, 1, 2, 2, 1, 0]
            }, {
                "name": '3rd place',
                "data": [3, 4, 2, 3, 2, 1, 1]
            }],
        }
    else:
        chart = {
            'xAxis': {'categories': [2014, 2015, 2016, 2017, 2018, 2019, 2020]},
            'yAxis': {"title": {"text": 'Win rate [%]'}},
            'series': [{"name": 'Win rate [%]',
                "data": [10, 40, 20, 60, 80, 100]}]
        }


    return JsonResponse(chart)
