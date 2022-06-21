import json
import requests
import base64
import pprint as p


def encode_b64(to_encode):
    encoded_ascii = to_encode.encode('ascii')
    base64_bytes = base64.b64encode(encoded_ascii)
    encoded_b64 = base64_bytes.decode('ascii')

    return encoded_b64


def list_workers(api_key):
    url = "https://onfleet.com/api/v2/workers?filter=name,id"
    payload = ""
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    # p.pprint(response)
    return response


def get_single_worker(api_key, workerid):
    url = f"https://onfleet.com/api/v2/workers/{workerid}?analytics=false"

    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    # print(response)
    return response


def list_tasks(api_key):
    tasks = []
    lastid = ()

    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }

    i = 1
    while i > 0:
        if i == 1:
            url = f"https://onfleet.com/api/v2/tasks/all?from=1455072025000"

            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

            lastid = response.get('lastId', '')

            tasks = tasks + response['tasks']

            i += 1

        elif lastid != "":

            url = f"https://onfleet.com/api/v2/tasks/all?from=1455072025000&lastId={lastid}"
            response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

            lastid = response.get('lastId', '')

            tasks = tasks + response['tasks']

            i += 1
        elif lastid == "":
            i = 0

    # p.pprint(tasks)
    return tasks


def get_single_task(api_key, task_id):
    url = f"https://onfleet.com/api/v2/tasks/{task_id}"

    payload = {}
    headers = {
        'Authorization': 'Basic ' + encode_b64(api_key)
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    return response
