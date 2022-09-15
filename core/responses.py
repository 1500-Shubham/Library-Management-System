from django.http.response import JsonResponse, HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta
import json, http.client


def init_response(res_str=None, data=None):
    """
    Initializes the response object
    both arguments are optional.
    """

    response = {}
    response["res_str"] = ""
    response["res_data"] = {}
    if res_str is not None:
        response["res_str"] = res_str
    if data is not None:
        response["res_data"] = data
    return response

###### sabse important hai kaise ho raha########
def _send(data, status_code):
    return JsonResponse(data=data, status=status_code)


def send_200(data, res_str=''):
    if res_str:
        data['res_str'] = res_str
    return _send(data, 200)


def send_201(data={}, res_str=''):
    if res_str:
        data['res_str'] = res_str
    return _send(data, 201)


def send_204(data):
    return _send(data, 204)


def send_302(url):
    return HttpResponseRedirect(url)


def send_302_auth_sso(url):
    res = HttpResponse(url, status=302)
    res['location'] = url
    return res


def send_400(data={}, res_str=''):
    if res_str:
        data['res_str'] = res_str
    return _send(data, 400)


def send_401(data):
    return _send(data, 401)


def send_403(data):
    return _send(data, 403)


def send_404(data):
    return _send(data, 404)


def send_410(data):
    return _send(data, 410)

def send_422(data):
    return _send(data, http.client.UNPROCESSABLE_ENTITY)

def send_451(data):
    return _send(data, 451)

def send_500(data):
    return _send(data, http.client.INTERNAL_SERVER_ERROR)

def send_502(data):
    return _send(data, 502)

def send_503(data):
    # Only to be used when under maintenance.
    return _send(data, 503)

def put_to_dict(put_body):
    """
    put_body: string of put body
    """
    dic = {}
    for item in put_body.split('&'):
        key_val = item.split("=")
        dic[key_val[0]] = key_val[1]
    return dic


def get_dict(put_body):
    return json.loads(put_body)

def send_202(data, res_str=''):
    if res_str:
        data['res_str'] = res_str
    return _send(data, 202)