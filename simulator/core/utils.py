from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Coroutine, List
import aiohttp
import asyncio
import plotly.graph_objects as go
from plotly.offline import plot
import datetime


def buildContext(**kwargs):
    return kwargs

"""Execute an GET http call async """
async def http_get(session: aiohttp.ClientSession, url: str) -> Coroutine:
    async with session.get(url) as response:
        resp = await response.json()
        return resp

"""Execute an POST http call async """
async def http_post(session: aiohttp.ClientSession, url: str, data : str) -> Coroutine:
    async with session.post(url,data) as response:
        resp = await response.json()
        return resp

#WRITE PUT AND DELETE AS WELL

async def fetch_all(urls: List, inner: Callable):
    """Gather many HTTP call made async """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                inner(
                    session,
                    url
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

def run():
    comments = [f"https://jsonplaceholder.typicode.com/comments/{id_}" for id_ in range(1,500)]
    responses = asyncio.get_event_loop().run_until_complete(fetch_all(comments, http_get))

#https://towardsdatascience.com/python-requests-api-70a555fecc97    

def multi_threading_runnder(function,data_list):
    threads = []
    result = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for data in data_list:
            threads.append(executor.submit(function,data))

            for task in as_completed(threads):
                result.append(task.result())


#https://creativedata.stream/multi-threading-api-requests-in-python/

def create_candle_stick(data):
        figure = go.Figure(
            data = [
                    go.Candlestick(
                    x =   [datetime.datetime.fromtimestamp( epoch_time )   for epoch_time in data['t']],
                      high = data['h'],
                      low = data['l'],
                      open = data['o'],
                      close = data['c'],
                    )
                  ]
        )
        candlestick_div = plot(figure, output_type='div')
        return candlestick_div