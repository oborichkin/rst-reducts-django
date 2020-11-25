from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='reducts-index'),
    path('find', views.ReductCalcView.as_view(), name='reducts-find'),
    path('quick', views.QuickReductCalcView.as_view(), name='reducts-quick')
]