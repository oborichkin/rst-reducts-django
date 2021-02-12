import time

from collections import defaultdict

from django.shortcuts import render
from django.views.generic import TemplateView

from define import make_qmt, classify
from define.algo import Step

from .forms import DatasetForm, DefineSystemForm
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


class DefineCalcView(TemplateView):
    template_name = "define.html"

    def get(self, request, *args, **kwargs):
        default_form = {
            "csv_train": "1,1,1,1,1,1,1,1,1,a\n1,1,2,2,1,1,2,1,1,a\n2,1,2,2,1,1,3,2,4,a\n2,1,2,4,1,1,3,2,4,a\n1,2,1,1,2,1,1,2,1,b\n1,2,3,3,2,1,3,1,1,b\n2,2,1,2,1,2,4,2,2,b\n2,3,4,4,1,1,3,2,2,c\n2,1,4,4,1,1,4,2,3,c\n3,4,5,3,3,3,1,3,4,d\n4,5,5,5,2,2,4,2,1,d\n3,5,5,1,2,1,5,2,5,d\n3,4,3,5,4,4,2,4,1,e\n4,2,3,3,2,4,2,2,1,e",
            "csv_test": "3,4,3,5,3,4,2,1,1\n4,4,3,3,2,4,2,3,5"
        }
        form = DefineSystemForm(initial=default_form)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = DefineSystemForm(request.POST)
        elapsed = 0
        try:
            train_list = [tuple(line.strip().split(",")) for line in form.data["csv_train"].split("\r\n")]
            train_dict = defaultdict(list)
            for element in train_list:
                train_dict[element[-1]].append(element[:-1])
            test_list = [tuple(line.strip().split(",")) for line in form.data["csv_test"].split("\r\n")]
            t0 = time.time()
            steps = Step()
            qmt_dict = make_qmt(train_dict, algo_steps=steps)
            qmt = []
            qmt.append([" "] + list(qmt_dict.keys()))
            steps = steps.html
            for i, i_elem in qmt_dict.items():
                qmt.append([i] + list(i_elem.values()))
            result = classify(train_dict, test_list)
            t1 = time.time()
            elapsed = t1 - t0
            errors = None
        except Exception as e:
            qmt = None
            steps = ""
            result = None
            errors = str(e)
        if form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "elapsed": elapsed,
                    "qmt": qmt,
                    "result": result,
                    "errors": errors,
                    "steps": steps
                }
            )

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