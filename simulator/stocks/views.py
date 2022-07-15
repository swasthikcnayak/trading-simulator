from django.shortcuts import render
from yahoo_fin.stock_info import tickers_nifty50, get_quote_table
from core.utils import buildContext
import queue
from threading import Thread
from rest_framework.decorators import api_view
from rest_framework.response import Response

def stock_picker(request):
    stock_picker = tickers_nifty50()
    context = buildContext(stocks=stock_picker)
    return render(request,'dashboard/stockpicker.html',context)


#update this to use thread pool
def stock_dispay(request):
    stockList = request.GET.getlist('stockpicker')
    stockshare = str(stockList)[1:-1]
    data = {}
    n_threads = len(stockList)
    thread_list = []
    que = queue.Queue()
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockList[i]: get_quote_table(arg1)}), args = (que, stockList[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()
    while not que.empty():
        data.update(que.get())
    context = buildContext(data=data,room_name='track',selectedstock=stockshare)
    return render(request,'dashboard/stockdisplay.html',context)

@api_view(["GET"])
def show_stock_suggestion_on_search(request):
    if request.method == "GET":
        data = ['hi','hello','brother','bro']
       #MAKE API CALL AND GET THE SUGGESTION
        return Response(data)

def search_stock(request):
    return render(request,'dashboard/stocksearch.html')