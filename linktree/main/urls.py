from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', view=views.IndexView.as_view(), name='index'),
    path('prices/', view=views.PricesView.as_view(), name='prices'),
    path('examples/', view=views.ExamplesView.as_view(), name='examples')
]