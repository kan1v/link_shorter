from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.response import TemplateResponse

class IndexView(TemplateView):
    template_name = 'main/index.html'

class PricesView(TemplateView):
    template_name = 'main/prices.html'

class ExamplesView(TemplateView):
    template_name = 'main/examples.html'