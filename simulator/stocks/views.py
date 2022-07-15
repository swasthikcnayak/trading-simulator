from django.shortcuts import render
from yahoo_fin.stock_info import tickers_nifty50, get_quote_table
from core.utils import buildContext
import queue
from threading import Thread

def stockPicker(request):
    stock_picker = tickers_nifty50()
    context = buildContext(stocks=stock_picker)
    return render(request,'dashboard/stockpicker.html',context)


#update this to use thread pool
def stockDispay(request):
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