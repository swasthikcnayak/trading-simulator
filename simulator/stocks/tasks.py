from celery import shared_task
from yahoo_fin.stock_info import get_quote_table
import queue
from threading import Thread
from channels.layers import get_channel_layer
import asyncio

#modify this to use thread pool instead of creating so unlimited threads
@shared_task(bind=True)
def update_stock(self,stockList):
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
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send("stock_track", {
        'type': 'send_stock_update',
        'message': data,
    }))
            
    return 'Done'