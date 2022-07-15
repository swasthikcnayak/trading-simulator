from django.urls import path
from stocks import views


urlpatterns = [
    path('stockdisplay/', views.stockDispay, name='stock-picker'),
    path('stockpicker/', views.stockPicker, name='stock-display')
]
