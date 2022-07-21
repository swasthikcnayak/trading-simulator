from django.urls import path
from stocks import views


urlpatterns = [
    path('stockdisplay/', views.stock_dispay, name='stock-picker'),
    path('stockpicker/', views.stock_picker, name='stock-display'),
    path('stock-suggestion/',views.show_stock_suggestion_on_search,name="show-stock-suggestion"),
    path('search-stock/',views.search_stock,name="search-stock"),
    path('stock-candlestick/<str:stock>',views.candle_stick_plot_view,name="candle-stick")
]
