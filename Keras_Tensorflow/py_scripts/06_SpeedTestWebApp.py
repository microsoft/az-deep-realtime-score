# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py_scripts//py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Load Test deployed web application

# This notebook pulls some images and tests them against the deployed web application. We submit requests asychronously which should reduce the contribution of latency.

# +
import asyncio
import json
import urllib.request
from timeit import default_timer

import aiohttp
import matplotlib.pyplot as plt
from testing_utilities import to_img, gen_variations_of_one_image, get_auth
from tqdm import tqdm
import requests
from dotenv import set_key, get_key, find_dotenv
from azureml.core.workspace import Workspace
from azureml.core.webservice import AksWebservice

# %matplotlib inline
# -

print(aiohttp.__version__)

env_path = find_dotenv(raise_error_if_not_found=True)

ws = Workspace.from_config(auth=get_auth())
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep="\n")

# Let's retrive the web service.

aks_service_name = get_key(env_path, 'aks_service_name')
aks_service = AksWebservice(ws, name=aks_service_name)

# We will test our deployed service with 100 calls. We will only have 4 requests concurrently at any time. We have only deployed one pod on one node and increasing the number of concurrent calls does not really increase throughput. Feel free to try different values and see how the service responds.

NUMBER_OF_REQUESTS = 100  # Total number of requests
CONCURRENT_REQUESTS = 4   # Number of requests at a time

# Get the scoring URL and API key of the service.

scoring_url = aks_service.scoring_uri
api_key = aks_service.get_keys()[0]

IMAGEURL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg"
plt.imshow(to_img(IMAGEURL))

# Here, we use varitions of the same image to test the service.

url_list = [[scoring_url, img_bytes] for img_bytes in gen_variations_of_one_image(IMAGEURL, NUMBER_OF_REQUESTS)]


def decode(result):
    return json.loads(result.decode("utf-8"))


async def fetch(url, session, data, headers):
    start_time = default_timer()
    async with session.request('post', url, data={'image':data}, headers=headers) as response:
        resp = await response.read()
        elapsed = default_timer() - start_time
        return resp, elapsed

async def bound_fetch(sem, url, session, data, headers):
    # Getter function with semaphore.
    async with sem:
        return await fetch(url, session, data, headers)

async def await_with_progress(coros):
    results=[]
    for f in tqdm(asyncio.as_completed(coros), total=len(coros)):
        result = await f
        results.append((decode(result[0]),result[1]))
    return results

async def run(url_list, num_concurrent=CONCURRENT_REQUESTS):
    # headers = {'content-type': 'application/json'}
    headers = {'Authorization':('Bearer '+ api_key)}
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(num_concurrent)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with aiohttp.ClientSession() as session:
        for url, data in url_list:
            # pass Semaphore and session to every POST request
            task = asyncio.ensure_future(bound_fetch(sem, url, session, data, headers))
            tasks.append(task)
        return await await_with_progress(tasks)

# Below we run the 100 requests against our deployed service.

loop = asyncio.get_event_loop()
start_time = default_timer()
complete_responses = loop.run_until_complete(asyncio.ensure_future(run(url_list, num_concurrent=CONCURRENT_REQUESTS)))
elapsed = default_timer() - start_time
print('Total Elapsed {}'.format(elapsed))
print('Avg time taken {0:4.2f} ms'.format(1000*elapsed/len(url_list)))

complete_responses[:3]

num_succesful=[i[0][0]['image'][0][0] for i in complete_responses].count('n02127052')
print('Succesful {} out of {}'.format(num_succesful, len(url_list)))

# Example response
plt.imshow(to_img(IMAGEURL))
complete_responses[0]

# To tear down the cluster and all related resources go to the [tear down the cluster](07_TearDown.ipynb) notebook.
