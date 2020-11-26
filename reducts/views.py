import time

from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import DatasetForm
from .logic import RoughSet, qreduct, reduct

temp_result = {
    "sample_data": [
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    ],
    "reducts": [
        [1, 2]
    ]
}

class IndexView(TemplateView):
    template_name = "index.html"

class ReductCalcView(TemplateView):
    template_name = "reducts.html"

    def get(self, request, *args, **kwargs):
        default_form = {
            "csv_string": "False,True,High,True\nTrue,False,High,True\nTrue,True,Very High,True\nFalse,True,Normal,False\nTrue,False,High,False\nFalse,True,Very High,True",
            "c_attributes": "0,1,2",
            "d_attributes": "3"
        }
        form = DatasetForm(initial=default_form)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = DatasetForm(request.POST)
        elapsed = 0
        try:
            dataset = [tuple([y for y in x.split(",")]) for x in form.data["csv_string"].split("\r\n")]
            c_attributes = set([int(x) for x in form.data["c_attributes"].split(",")])
            d_attributes = set([int(x) for x in form.data["d_attributes"].split(",")])
            r = RoughSet(dataset)
            t0 = time.time()
            result = [set(x) for x in reduct(r, c_attributes, d_attributes)]
            t1 = time.time()
            sample_data = dataset[:min(len(dataset),5)]
            errors = None
            elapsed = t1 - t0
        except Exception as e:
            sample_data = None
            result = None
            errors = str(e)
        if form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "elapsed": elapsed,
                    "sample_data": sample_data,
                    "reducts": result,
                    "errors": errors
            })

class QuickReductCalcView(TemplateView):
    template_name = "qreducts.html"

    def get(self, request, *args, **kwargs):
        default_form = {
            "csv_string": "False,True,High,True\nTrue,False,High,True\nTrue,True,Very High,True\nFalse,True,Normal,False\nTrue,False,High,False\nFalse,True,Very High,True",
            "c_attributes": "0,1,2",
            "d_attributes": "3"
        }
        form = DatasetForm(initial=default_form)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = DatasetForm(request.POST)
        elapsed = 0
        try:
            dataset = [tuple([y for y in x.split(",")]) for x in form.data["csv_string"].split("\r\n")]
            c_attributes = set([int(x) for x in form.data["c_attributes"].split(",")])
            d_attributes = set([int(x) for x in form.data["d_attributes"].split(",")])
            r = RoughSet(dataset)
            t0 = time.time()
            result = [qreduct(r, c_attributes, d_attributes)]
            t1 = time.time()
            sample_data = dataset[:min(len(dataset), 5)]
            errors = None
            elapsed = t1 - t0
        except Exception as e:
            sample_data = None
            result = None
            errors = str(e)
        if form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "elapsed": elapsed,
                    "sample_data": sample_data,
                    "reducts": result,
                    "errors": errors
            })